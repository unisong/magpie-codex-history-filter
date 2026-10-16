"""Optional Windows Magpie smoke test; all upstream traffic stays on loopback."""
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import json
import os
import shutil
import socket
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--binary", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
seen = []


class Mock(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        seen.append(body)
        reply = json.dumps({"id": "resp_mock", "object": "response", "status": "completed",
                            "model": body["model"], "output": []}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)


mock = ThreadingHTTPServer(("127.0.0.1", 0), Mock)
threading.Thread(target=mock.serve_forever, daemon=True).start()
scratch = Path(tempfile.mkdtemp(prefix="magpie-history-smoke-")).resolve()
app = scratch / "app"
app.mkdir()
binary = app / "magpie.exe"
shutil.copy2(Path(args.binary).resolve(), binary)
(app / ".portable").write_text("")
data = app / "data"
data.mkdir()
home = scratch / "profile"
home.mkdir()
with socket.socket() as port_socket:
    port_socket.bind(("127.0.0.1", 0))
    port = port_socket.getsockname()[1]
origin = f"http://127.0.0.1:{port}"
(data / "settings.json").write_text(json.dumps({"port": port, "updateEvery": 1440}))
(data / "plugins.yml").write_text("preset: all\n")
(data / "providers.json").write_text(json.dumps({"providers": [
    {"id": pid, "name": pid, "key": "LOCAL_MOCK_ONLY",
     "responses": f"http://127.0.0.1:{mock.server_port}/v1", "models": ["gpt-6-astra"]}
    for pid in ("demo", "backup")
]}))
rule = {"historyFilter": True, "preserveEncryptedInclude": True}
plugin = {"plugins": [{"spec": str(root), "options": {
    "providers": {"magpie:demo": rule}, "aliases": {"old-demo": "demo"}}}]}
plugin_file = data / "plugins.json"
plugin_file.write_text(json.dumps(plugin))
env = {k: v for k, v in os.environ.items() if k.upper() in
       ("SYSTEMROOT", "WINDIR", "PATH", "TEMP", "TMP", "PATHEXT", "COMSPEC")}
env.update({"USERPROFILE": str(home), "XDG_CONFIG_HOME": str(scratch / "config"),
            "XDG_CACHE_HOME": str(scratch / "cache"), "MAGPIE_ADDR": f"127.0.0.1:{port}"})
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
log = (scratch / "magpie.log").open("wb")
proc = None


def post(body):
    req = urllib.request.Request(origin + "/v1/responses",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        response = opener.open(req, timeout=12)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        return response.status, response.read().decode()


try:
    proc = subprocess.Popen([str(binary), "serve"], cwd=app, env=env, stdout=log, stderr=log,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    for _ in range(100):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                break
        except OSError:
            if proc.poll() is not None:
                raise RuntimeError(f"Magpie exited; inspect {scratch}")
            time.sleep(0.1)
    else:
        raise RuntimeError(f"Gateway did not start; inspect {scratch}")
    history = [{"type": "reasoning", "id": "rs_foreign", "encrypted_content": "foreign"},
               {"type": "message", "id": "msg_foreign", "role": "user", "content": "Mock only."}]
    body = {"model": "demo/gpt-6-astra", "input": history,
            "include": ["reasoning.encrypted_content"], "stream": False}
    status, response = post(body)
    assert status == 200, (status, response)
    assert len(seen[-1]["input"]) == 1 and "id" not in seen[-1]["input"][0], seen[-1]
    assert seen[-1]["store"] is False
    assert seen[-1]["include"] == ["reasoning.encrypted_content"]
    print("PASS real middleware rewrites history before mock upstream")
    status, response = post({**body, "model": "backup/gpt-6-astra"})
    assert status == 200, (status, response)
    assert any(i.get("type") == "reasoning" for i in seen[-1]["input"])
    print("PASS unconfigured supplier remains unfiltered")
    calls = len(seen)
    status, response = post({**body, "previous_response_id": "resp_foreign"})
    assert status == 400 and "Codex history filter:" in response
    assert len(seen) == calls
    print("PASS unsafe reference is rejected before upstream")
    status, response = post({**body, "model": "old-demo/gpt-6-astra", "previous_response_id": "resp_foreign"})
    assert status == 400 and "Codex history filter:" in response
    assert len(seen) == calls
    print("PASS alias selects the rule inside the real runtime")
    plugin["plugins"][0]["options"]["providers"]["magpie:backup"] = {
        "historyFilter": True, "preserveEncryptedInclude": False}
    plugin_file.write_text(json.dumps(plugin))
    time.sleep(1.2)
    status, response = post({**body, "model": "backup/gpt-6-astra"})
    assert status == 200, (status, response)
    assert len(seen[-1]["input"]) == 1 and "reasoning.encrypted_content" not in seen[-1].get("include", [])
    print("PASS hot-reloaded second supplier has independent options")
    assert (data / "providers.json").exists()
    assert not (home / ".codex/config.toml").exists()
    print(json.dumps({"passed": True, "mockCalls": len(seen), "realSupplierCalls": 0,
                      "scratch": str(scratch)}))
finally:
    if proc is not None:
        proc.terminate()
        proc.wait(timeout=10)
    log.close()
    mock.shutdown()
    mock.server_close()
