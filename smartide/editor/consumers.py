import asyncio
import json
import subprocess
import tempfile
from channels.generic.websocket import AsyncWebsocketConsumer


class TerminalConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.process = None

    async def disconnect(self, close_code):
        if self.process:
            self.process.kill()

    async def receive(self, text_data):
        data = json.loads(text_data)

        if "code" in data:
            code = data["code"]

            if self.process:
                self.process.kill()

            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
            temp.write(code)
            temp.close()

            self.process = subprocess.Popen(
                ["python", "-u", "-i", temp.name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            asyncio.create_task(self.read_output())

        elif "input" in data:
            if self.process:
                try:
                    self.process.stdin.write(data["input"])
                    self.process.stdin.flush()
                except:
                    pass

    # ✅ THIS MUST BE INSIDE CLASS
    async def read_output(self):
        loop = asyncio.get_event_loop()

        while True:
            if self.process is None:
                break

            output = await loop.run_in_executor(
                None, self.process.stdout.read, 1
            )

            if not output:
                break

            await self.send(text_data=json.dumps({
                "output": output
            }))