# 项目结构

> 根目录：`d:\下载数据\11`

```text
d:\下载数据\11
├── README.md                       # 项目说明
├── render.yaml                     # Render 部署配置（根）
├── .gitignore
│
│  # —— 宠物兔术后康复衣图纸（Python + 生成的 PNG，与生日网站无关）——
├── miaoda-code-三视图绘制源码（Python）.py
├── miaoda-code-样板裁片图绘制源码（Python）.py
├── miaoda-code-流程图绘制源码（Python）.py
├── pattern_pieces-样板裁片图.py
├── recovery_suit_three_views.png
├── recovery_suit_pattern_pieces.png
└── recovery_suit_flowchart.png
│
├── frontend/                       # Vue 3 + Vite + TS 前端
│   ├── index.html
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── pnpm-workspace.yaml
│   ├── vite.config.ts
│   ├── tsconfig.json / tsconfig.app.json / tsconfig.node.json
│   ├── .env.example / .env.production.example
│   ├── netlify.toml
│   ├── Christina Perri - A Thousand Years.mp3 / .ncm   # 背景音乐文件
│   ├── public/
│   │   └── _redirects
│   ├── src/
│   │   ├── main.ts                # 入口
│   │   ├── App.vue
│   │   ├── vite-env.d.ts
│   │   ├── api/index.ts           # axios 封装与接口
│   │   ├── config/site.ts         # 内容配置（寿星/祝福/相册/信件）
│   │   ├── stores/birthday.ts     # Pinia 状态（含离线兜底）
│   │   ├── router/index.ts
│   │   ├── types/index.ts         # TS 类型定义
│   │   ├── styles/main.scss       # 全局样式与配色变量
│   │   ├── views/HomeView.vue     # 首页（组合各区块）
│   │   └── components/            # 12 个区块组件
│   │       ├── LoadingOverlay.vue
│   │       ├── StarField.vue
│   │       ├── Balloons.vue
│   │       ├── MusicButton.vue
│   │       ├── HeroSection.vue
│   │       ├── CakeSection.vue
│   │       ├── CelebrationCanvas.vue
│   │       ├── BlessingSection.vue
│   │       ├── AlbumSection.vue
│   │       ├── MessageWall.vue
│   │       ├── LetterSection.vue
│   │       └── FinaleSection.vue
│   ├── dist/                      # 构建产物（已生成）
│   └── node_modules/              # 依赖（已安装）
│
└── backend/                        # Spring Boot 3 + Java 17 后端
    ├── pom.xml
    ├── Dockerfile
    ├── render.yaml
    ├── data/                       # H2 文件数据库（本地持久化）
    │   ├── birthday.mv.db
    │   └── birthday.lock.db
    ├── database/
    │   └── init-mysql.sql          # MySQL 生产初始数据
    ├── src/
    │   ├── main/java/com/example/birthday/
    │   │   ├── BirthdayApplication.java
    │   │   ├── config/
    │   │   │   ├── CorsConfig.java
    │   │   │   └── DataInitializer.java
    │   │   ├── common/
    │   │   │   ├── ApiResponse.java
    │   │   │   ├── BusinessException.java
    │   │   │   └── GlobalExceptionHandler.java
    │   │   ├── controller/
    │   │   │   └── BirthdayController.java
    │   │   ├── service/
    │   │   │   └── BirthdayService.java
    │   │   ├── repository/
    │   │   │   ├── BirthdayInfoRepository.java
    │   │   │   ├── BirthdayMessageRepository.java
    │   │   │   ├── MessageLikeRepository.java
    │   │   │   └── VisitStatRepository.java
    │   │   ├── domain/
    │   │   │   ├── BirthdayInfo.java
    │   │   │   ├── BirthdayMessage.java
    │   │   │   ├── MessageLike.java
    │   │   │   └── VisitStat.java
    │   │   └── dto/
    │   │       ├── BirthdayInfoResponse.java
    │   │       ├── BirthdayMessageResponse.java
    │   │       ├── CreateMessageRequest.java
    │   │       ├── PageResponse.java
    │   │       └── StatsResponse.java
    │   ├── main/resources/
    │   │   ├── application.yml
    │   │   ├── application-h2.yml
    │   │   ├── application-mysql.yml
    │   │   ├── application-postgres.yml
    │   │   ├── schema.sql
    │   │   └── data.sql
    │   └── test/java/com/example/birthday/
    │       └── BirthdayControllerIntegrationTest.java
    └── target/                     # 构建产物（已生成，含 birthday-wish-api-1.0.0.jar）
```

## 说明

- 顶层还有几个工具/IDE 目录未列入上方树中：`.git`、`.idea`、`.agents`、`.tools`、`.venv`（Python 虚拟环境，供绘图脚本使用），不影响运行逻辑。
- `backend/target/` 里已有构建好的 `birthday-wish-api-1.0.0.jar`，说明后端已成功编译过。
