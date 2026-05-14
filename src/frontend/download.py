import urllib.request
url = "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2VhZWJlNDhlNmYxNTQ2M2M4ZTNkYzNkNjhjODgzODM1EgsSBxCd6cvk-hsYAZIBIwoKcHJvamVjdF9pZBIVQhMzNjU3NjkyNTUyNjEwNTI5MTQ3&filename=&opi=96797242"
output_path = r"c:\Users\andre\Documents\VSC Projects\vibecoding\src\frontend\stitch_dashboard_mockup.html"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Download successful")
except Exception as e:
    print(f"Error: {e}")
