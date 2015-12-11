
consumer_key = "IgcSZd675nvisCYIYOXt9Rfnz";
consumer_secret = "R1D1quBUooIGUDoBtaIkKnfFdI4AUaOloME4y72DU4YNmwvCTV";
access_token = "4050176059-Dk4YFqIxc5ojG3bvBLsqIeNI36gqqVaWFhXZJHl";
access_token_secret = "NlYxAbWyMbSIVsuDpFwJSFxzUeTTKdIAYkGnXuv6v7ou1";

twitter_credentials = {
    "consumer_key"        :  consumer_key,
    "consumer_secret"     :  consumer_secret,
    "access_token"        :  access_token,
    "access_token_secret" :  access_token_secret,
}



def auth_get(auth_key):
    if auth_key in twitter_credentials:
        return twitter_credentials[auth_key]
    return None
