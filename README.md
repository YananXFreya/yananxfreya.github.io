# 辛雅楠的个人主页 / Yanan Xin

访问地址：**https://yananxfreya.github.io/**

基于 [Lab Website Template](https://github.com/greenelab/lab-website-template) 的个人主页静态改版，包含完整中文、英文版本。保留上游样式模块、论文卡片结构和 BSD 3-Clause 许可证，详见 [模板来源](theme/lab-website-template/README.md)。不需要 Jekyll、Ruby 或付费服务。

## 修改文字

1. 编辑 `content/site.json`。双语字段包含 `zh` 与 `en`，请同步修改并更新 `updated` 日期。
2. 在项目目录运行 `python tools/build_site.py`（Python 3.12 或更新版本，无第三方依赖）。
3. 运行 `python -m http.server 8000`，浏览器访问 `http://localhost:8000/` 预览。请通过 HTTP 预览，直接双击 HTML 无法正确解析根路径。
4. 检查后将内容文件及生成的 HTML 一起提交、推送到 `main`。GitHub Pages 从 `main` 根目录发布。

`index.html` 是默认中文首页；`zh/` 与 `en/` 各含首页、教育、成果、研究、资源收藏、联系页面。优先编辑内容源文件，直接修改生成的 HTML 会在下次构建时被覆盖。

## 添加收藏资源

- 在 `content/site.json` 的 `resources` 中按主题分组，在相应分组的 `items` 中增加资源。
- 为每条资源填写唯一 `id`、双语标题与简介、来源、作者、原站 URL、关键词及常用章节链接。
- 收藏页位于 `/zh/resources/` 与 `/en/resources/`，主导航提供入口；运行同一构建脚本即可更新页面和站点地图。
- 简介使用自己的概括，保留原作者与原站链接；未经许可不转载外部讲义或 PDF。

## 添加论文与图表

- 在 `content/site.json` 的 `papers` 中增加条目；`id` 唯一且只使用小写英文、数字和短横线。
- 核对完整作者、年份、成果类型、DOI 与正式记录。没有确认的 DOI 时使用空字符串。
- `title` 为英文原题，`title_zh` 为中文译名；摘要和图片说明维护两种语言。
- 将适合公开的图表导出到 `assets/images/`，填写 `figures`。保留完整坐标、单位、图例，不重新生成研究数据。
- 当前图像由作者提供的 PDF 原图完整页面无损导出为 WebP，宽约 2000 像素；点击可查看原尺寸。
- 本站展示精选合作研究，会议论文与会议海报分别标注。不根据作者顺序推断特殊署名身份。

## 更新公开简历

两份下载文件从已核对的公开信息重新制作，不是原始求职简历。

```powershell
python -m pip install reportlab
python tools/build_cv.py
```

脚本读取 `content/site.json`，输出 `assets/cv/yanan-xin-zh.pdf` 和 `yanan-xin-en.pdf`。Windows 默认使用已安装的微软雅黑字体；其他系统请将 `CV_CJK_FONT` 环境变量设置为支持中文的 TrueType 字体路径。字体不随仓库分发。

也可用自行制作、检查过的公开简历替换同名文件。更新后检查分页、文字、链接和隐私内容。

## 样式与交互

- `assets/site.css`：个人布局、颜色和响应式样式。
- `assets/site.js`：语言偏好及手机导航。仅根路径恢复偏好；明确访问 `/zh/` 或 `/en/` 时尊重 URL。存储受限或 JavaScript 关闭时，语言链接仍可使用。
- `tools/build_site.py`：页面模板、导航、页脚和元数据。
- `assets/template.css`：上游样式编译结果；源文件位于 `theme/lab-website-template/`，通常无需修改。

## 发布与回退

`.nojekyll` 使 GitHub Pages 直接提供静态文件。保持发布来源为 `main` 分支根目录。

初始站点提交：`327bf114d89a59892404906870107f8c328305db`。改版前版本保存在 `backup-before-personalization-20261122` 分支。需要回退时，可在 Pages 设置中切换至备份分支根目录，无需删除代码或重写 Git 历史。

## 公开资料范围

仓库只保存网站源码、公开文案、选定论文图表和两份公开简历。原始学历证书、完整求职简历、论文 ZIP、LaTeX 工程、本地核对记录和账号凭据不属于发布内容。

模板代码遵循 [BSD 3-Clause](LICENSE.md)。论文图表和个人资料的权利归其原作者及相应权利人；模板许可证不改变这些材料的权利归属。
