@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================================
echo   [SANDBOX] QURAN VISION TEST ORTAMI (v6.3.0-beta.1 ^| localhost:8080)
echo   Klasor : %~dp0docs
echo   Adres  : http://localhost:8080
echo ============================================================================
start http://localhost:8080
python -X utf8 -c "import sys, http.server, functools, socket, time; exec('class H(http.server.SimpleHTTPRequestHandler):\n def copyfile(self, s, o):\n  self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)\n  mv = memoryview(s.read())\n  for i in range(0, len(mv), 16384): self.request.sendall(mv[i:i+16384])\n  time.sleep(0.05)\nclass S(http.server.ThreadingHTTPServer):\n address_family = socket.AF_INET6\n def server_bind(self):\n  self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)\n  return super().server_bind()\nS((sys.argv[2], 8080), functools.partial(H, directory=sys.argv[1])).serve_forever()')" docs ::
pause
