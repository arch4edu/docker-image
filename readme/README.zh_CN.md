欢迎使用 arch4edu docker 镜像！
====

### 常见问题

* 如何搜索/安装一个包？

默认的包管理器是`pacman`。
你可以通过`pacman -Ss [搜索内容]`来搜包，
然后通过`pacman -S [包名]`来装一个特定的包。

* `pacman`安装包的时候下载报错 404 了

[**推荐**] 通过`pacman -Syu`更新并重启；或者用最新的 arch4edu docker 镜像开一个新的。

[**不推荐**] 只通过`pacman -Sy`来更新包数据库来获得最新的下载链接。

* 如何适配`nvidia-docker`？

安装版本号对应（可通过`lsblk`查看）的`nvidia-utils`即可。

* `pacman`中有的包没有怎么办？

如果有明确的软件包需求请到 [arch4edu](https://github.com/arch4edu/arch4edu) 提 Package request。

* 如何安装 Anaconda ？

简言之，不要装。如果你有软件包需求且`pacman`搜不到的话，请到 [arch4edu](https://github.com/arch4edu/arch4edu) 提 Package request。

* 如何装一个新的 Python 包？

请先通过`pacman -Ss python [Python 包名]`搜索。
如果没有的话，你可以通过`pip install --user [Python 包名]`安装

* 如何使用/配置某软件包？

请自行 [Google](https://www.google.com.hk) 或搜索 [ArchWiki](https://wiki.archlinux.org)

* 如何从 [AUR](https://aur.archlinux.org) 自行编译某软件包？

建议到 [arch4edu](https://github.com/arch4edu/arch4edu) 提 Package request。
如果真的要自行打包的话，请自行创建一个非 root 用户并使用 `devtools` 中的 `extra-x86_64-build` 命令打包。

* `systemd`不工作？

嗯，手动启动服务吧

* 哪里有 Archlinux 学习/讨论群？

[#archlinux-cn @Telegram](https://t.me/archlinuxcn_group)
[#archlinux-cn-offtopic @Telegram](https://t.me/archlinuxcn_offtopic)
