import subprocess

input_url = 'https://manifest.prod.boltdns.net/manifest/v1/hls/v4/clear/5348771529001/9121e6c9-bcfb-4b25-96c7-274eacde34b4/10s/master.m3u8?fastly_token=NjU0YmRhYjNfMDYwYjlkNTExOGE1OWJhZDVmOWMxYTRiZjgzYjYxMGVjNjA3ZGY0NDgzOGVmOTFkODkxMmVhNjk2NWU4YTgwZQ%3D%3D'
output_file = 'output.mp4'

# Specify the full path to the streamlink executable
streamlink_path = r'C:\Users\dee.HFMLEGAL\AppData\Roaming\Python\Python311\Scripts\streamlink.exe'  # Replace with the actual path

# Use streamlink with the full path to the executable
subprocess.run([streamlink_path, input_url, 'best', '-o', output_file])

print(f'Conversion completed. Output file: {output_file}')
