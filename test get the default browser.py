import winreg

def get_default_browser_name():
    try:
        # Open registry key for HTTP protocol
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice") as key:
            browser_prog_id, _ = winreg.QueryValueEx(key, "ProgId")

        # Mapping common ProgId values to actual browser names
        browser_map = {
            "ChromeHTML": "Chrome",
            "MSEdgeHTM": "Edge",
            "FirefoxURL": "Firefox",
            "OperaStable": "Opera",
            "BraveHTML": "Brave"
        }

        # Get browser name from mapping or return the raw ProgId if unknown
        return browser_map.get(browser_prog_id, browser_prog_id)
    
    except Exception:
        return "Unknown"

if __name__ == "__main__":
    browser_name = get_default_browser_name()
    print(f'{browser_name.lower()}.exe')
