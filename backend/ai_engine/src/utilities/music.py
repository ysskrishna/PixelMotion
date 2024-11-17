import random

data = [{
    "name":"Deep In Trance",
    "link":"https://music.wixstatic.com/preview/e102c1_916abfabecba4855a7b15e634d74ff18-128.mp3",
    "tags": ["Energy"]
},
{
    "name":"Ecstasy",
    "link":"https://music.wixstatic.com/preview/e102c1_78b3d4f810cf44be9b32b65ebd2086da-128.mp3",
    "tags": ["Energy"]
},
{
    "name":"Work It",
    "link":"https://music.wixstatic.com/preview/e102c1_b2a7e9cd08c54f9eb23154b132a1ac06-128.mp3",
    "tags": ["Energy"]
},
{
    "name":"Slammin'",
    "link":"https://music.wixstatic.com/preview/e102c1_76c82ff6fbeb499ab6e858e3e10594c6-128.mp3",
    "tags": ["Energy"]
},
{
    "name":"Heavy Hitter",
    "link":"https://music.wixstatic.com/preview/e102c1_c39b120ee19f49888d316e192f2470d4-128.mp3",
    "tags": ["Energy"]
},
{
    "name":"Punching Bag",
    "link":"https://music.wixstatic.com/preview/e102c1_e0f8b32a4b354f7da1044156ea403ab4-128.mp3",
    "tags": ["Energy"]
},
{
    "name":"Soul Train",
    "link":"https://music.wixstatic.com/preview/e102c1_fe3ac74c0ed341ddb7026f3ce9fb3dea-128.mp3",
    "tags": ["Energy"]
},
{
    "name":"Travelling Man",
    "link":"https://music.wixstatic.com/preview/e102c1_cac217250557443ebc185b65dcc090f2-128.mp3",
    "tags": ["Energy"]
},
{
    "name":"Upstep",
    "link":"https://music.wixstatic.com/preview/e102c1_155ce722db904d71baa35f4aa902409c-128.mp3",
    "tags": ["Energy"]
},
{
    "name":"Feelin' Good",
    "link":"https://music.wixstatic.com/preview/e102c1_a2d9db96691e4e7f8af9047b4b1eb218-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"Sunbeam",
    "link":"https://music.wixstatic.com/preview/e102c1_f8224d2940f04d8aa1101f6737fc0f52-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"Make It So",
    "link":"https://music.wixstatic.com/preview/e102c1_a1186e5fe80342e5b1e14cce1cb092f5-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"Open Road",
    "link":"https://music.wixstatic.com/preview/e102c1_c2abf912fb3c49738b838d6ac892fa3f-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"Passport",
    "link":"https://music.wixstatic.com/preview/e102c1_e108042556b94f75b1ffd85b3fe469d8-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"Love Life",
    "link":"https://music.wixstatic.com/preview/e102c1_b44c4141aea1439baca65657fe61a4e1-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"One Fine Summer",
    "link":"https://music.wixstatic.com/preview/e102c1_743d155392114036a1ae62f9d42be909-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"Reach Out",
    "link":"https://music.wixstatic.com/preview/e102c1_afb6754df76d4fb3841bf41276295b48-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"Up Your Street",
    "link":"https://music.wixstatic.com/preview/e102c1_e20b53eb23654ace9e9e5429622a42ec-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"Enterprise",
    "link":"https://music.wixstatic.com/preview/e102c1_6ccd4048a4fa4cecb04230b3398dd89e-128.mp3",
    "tags": ["Upbeat"]
},
{
    "name":"The Big One",
    "link":"https://music.wixstatic.com/preview/e102c1_155ce722db904d71baa35f4aa902409c-128.mp3",
    "tags": ["Upbeat"]
}]


def select_music() -> str:
    return random.choice(data)['link']
