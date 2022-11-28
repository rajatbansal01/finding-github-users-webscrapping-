from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests
from typing import List, Optional
import uvicorn


class input_params(BaseModel):
    l: Optional[str]
    q: Optional[str]
    type: Optional[str]


app = FastAPI()


@app.post("/userinfo")
def main(input_params: input_params):
    parmas = {"q": "hackathon location:india language:python", "type": "Users"}
    for key, value in input_params.dict().items():
        if value is not None:
            parmas[key] = value
    base_url = "https://github.com/search"
    response = requests.get(base_url, params=parmas)
    data_all = {}
    soup = BeautifulSoup(response.text, "html.parser")
    all_users = soup.findAll(
        "div", {"class": "d-flex hx_hit-user px-0 Box-row"})
    for i in range(len(all_users)):
        data_single = {"name": "", "github_handle": "", "blurb": "",
                       "location": "", "email": "", "github_url": ""}
        data_single["name"] = all_users[i].find("a", {"class": "mr-1"}).text
        data_single["github_handle"] = all_users[i].find(
            "a", {"class": "mr-1"}).get("href").split("/")[1]
        data_single["github_url"] = "https://github.com" + \
            "/" + data_single["github_handle"]
        try:
            data_single["email"] = all_users[i].find(
                "a", {"class": "Link--muted"}).text.strip()
        except:
            pass
        try:
            data_single["blurb"] = all_users[i].find(
                "p", {"class": "mb-1"}).text.strip()
        except:
            pass
        try:
            data_single["location"] = all_users[i].find(
                "div", {"class": "mr-3"}).text.strip()
        except:
            pass
        data_all[i] = data_single
    print(data_all)
    return data_all


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
