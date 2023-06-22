# Configuration File

# It is used to reuse generated session. DON'T CHANGE IT.
_DEFAULT_SESSION = None

_USER_AGENTS = ["Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 Instagram 12.0.0.16.90 (iPhone9,4; iOS 10_3_3; en_US; en-US; scale=2.61; gamut=wide; 1080x1920",
                "Instagram 121.0.0.29.119 Android (26/8.0.0; 480dpi; 1080x2032; HUAWEI; FIG-LX1; HWFIG-H; hi6250; en_US; 185203708)"]

# Minimum requests to make before shuffling a session
MIN_REQUESTS = 3

# Maximum requests to make before shuffling a session
MAX_REQUESTS = 6

# Maximun number of retries for each request
MAX_RETRIES = 3

# request timeout - in seconds
TIMEOUT = 5

# Example {"http":"proxy_here","https":"proxy_here"} Accepts python dictionary.
PROXY = None

# Directory to save and load logged in sessions/cookies
SESSION_DIRECTORY = "Insta Saved Sessions"


if __name__ == '__main__':
    pass
