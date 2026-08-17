# Birthday Wish

一个手机优先的生日祝福网站，前端使用 Vue 3 + Vite + TypeScript，后端使用 Spring Boot 3 + Java 17。前端默认带本地预览数据，后端未启动时也可以直接查看祝福、动画和留言墙；启动后端后可获得接口数据、分页留言、点赞和访问统计。

## 目录

```text
.
├── frontend/   Vue 3 前端
├── backend/    Spring Boot 后端
└── README.md
```

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`。如果要连接后端，复制 `.env.example` 为 `.env`，并按需修改：

```env
VITE_API_BASE_URL=http://localhost:8080/api
```

生产构建：

```bash
npm run build
npm run preview
```

## 后端启动

本地开发默认使用 H2 内存数据库，无需安装 MySQL：

```bash
cd backend
mvn spring-boot:run
```

接口根地址：`http://localhost:8080/api`

使用 MySQL：

```bash
cd backend
mvn spring-boot:run -Dspring-boot.run.profiles=mysql
```

MySQL 环境变量示例：

```env
MYSQL_URL=jdbc:mysql://localhost:3306/birthday_wish?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai&useSSL=false&allowPublicKeyRetrieval=true
MYSQL_USERNAME=root
MYSQL_PASSWORD=your-password
```

首次使用 MySQL 时，先创建数据库 `birthday_wish`，再执行：

```bash
mysql -u root -p birthday_wish < backend/src/main/resources/schema.sql
mysql -u root -p birthday_wish < backend/database/init-mysql.sql
```

## 内容替换位置

### 前端

- `frontend/src/config/site.ts`
  - `FALLBACK_BIRTHDAY_INFO`：寿星名字、生日日期、标题、祝福语、贺卡文案、音乐链接。
  - `BLESSING_LINES`：祝福区逐条文字。
  - `PHOTO_ITEMS`：相册照片，可把 `src` 改成本地图片或远程图片地址。
  - `FALLBACK_MESSAGES`：后端不可用时的本地留言。
- `frontend/src/styles/main.scss`
  - 全局配色变量，可替换午夜蓝、香槟金、珊瑚粉、奶油白等颜色。

### 后端

- `backend/src/main/resources/data.sql`：H2 开发环境的初始生日配置和留言。
- `backend/database/init-mysql.sql`：MySQL 生产环境初始数据。
- `backend/src/main/resources/application.yml`：CORS 允许来源。
- `backend/src/main/resources/application-mysql.yml`：MySQL 连接配置。

## 接口

统一响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/api/birthday/info` | 获取生日配置 |
| `GET` | `/api/messages?page=0&size=30` | 分页获取已展示留言 |
| `POST` | `/api/messages` | 提交祝福留言 |
| `POST` | `/api/messages/{id}/like` | 点赞留言 |
| `GET` | `/api/stats` | 获取访问量、留言数、点赞总数 |

`POST /api/messages` 请求体：

```json
{
  "senderName": "小林",
  "relationship": "朋友",
  "content": "祝你生日快乐，每天开心。"
}
```

点赞接口使用 `X-Visitor-Id` 请求头防止重复点赞。前端会在浏览器 `localStorage` 中自动生成访客 ID。

## 验证

后端测试：

```bash
cd backend
mvn test
```

覆盖内容：

- 生日配置接口正常返回。
- 留言创建成功。
- 过短留言被校验拦截。
- 同一访客重复点赞返回 `409`。

前端验证建议：

1. 打开 `http://localhost:5173`，确认加载动画约 2 到 3 秒后进入首页。
2. 点击蛋糕或开启麦克风吹气，确认蜡烛熄灭、烟花和祝福卡出现。
3. 提交留言并点赞，刷新页面后确认本地或后端数据保留。
4. 在移动端浏览器检查文字不溢出，平滑滚动自动降级为原生滚动。

## 生产部署建议

1. 前端构建后放入 Nginx，API 请求通过 `/api` 反向代理到 Spring Boot。
2. 后端使用 `application-mysql.yml`，并通过环境变量注入数据库密码。
3. 生产环境建议关闭 H2 控制台，开启 HTTPS，并使用独立数据库账号。
4. 如果照片较多，建议将相册图片放入对象存储或 CDN，不在前端包内堆放大文件。
