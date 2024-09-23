# FastAPI挂载静态资源

### 使用场景：前后端不分离，后端挂载图片，css,js等静态资源，给客户端响应html页面

###     首先假设项目根目录为app，app目录下的static为存放静态资源的目录

```python
#app/main.py
from fastapi import FastAPI

app = FastAPI()

#挂载静态资源
app.mount("/static", StaticFiles(directory="app/static"), name="static")
```

  如上即可成功挂载

### 在app目录的view为html页面资源

```
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
template = Jinja2Templates(r"app/views")

@router.get("/index", response_class=HTMLResponse)
def index(request: Request):
    return template.TemplateResponse("index.html", context={"request": request})

```



