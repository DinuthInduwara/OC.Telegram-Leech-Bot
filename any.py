import json
import asyncio


url = "https://www.youtube.com/watch?v=cO39Rmib-BI"
command_to_exec = [
                "yt-dlp",
                "--no-warnings",
                "--youtube-skip-dash-manifest",
                "-j",
                url
]

async def testing():
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
            # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    t_response = stdout.decode().strip()
    response_json = json.loads(t_response)

    output= []
    if "formats" in response_json:
        for formats in response_json["formats"]:
            format_id = formats.get("format_id")
            format_string = formats.get("format_note")
            format_ext = formats.get("ext")
            approx_file_size = ""
            if format_string.strip() == "storyboard":
                continue
            if "filesize" in formats:
                if formats["filesize"] == '' or formats["filesize"] == None:
                    continue
                approx_file_size = formats["filesize"]


            output.append({
                "size": approx_file_size,
                "format_id": format_id,
                "ext": format_ext,
                "quility": format_string
            })
        print(output)
        return output

asyncio.run(testing())


