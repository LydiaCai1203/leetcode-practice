## 将项目从mesos迁移到k8s流程简述


### 概述
    Marathon + Mesos(old) --> k8s(new)

### 发布流程
    project->post->mesos
    helm 文件配置文件管理服务
    
    用git仓库里的描述文件job 完成这个渲染的动作
    marathon(json)->k8s(yaml)  # 配置文件的转换

    修改gitlab文件的内容 以及 环境变量

### gitlab文件配置
    默认日志配置文件不需要额外进行 job渲染以后自动完成
    required 0.1cpu limits 1cpu
    请求到足够的资源以后会进行健康检查（readiness+liveness）前一个失败pod实例就会退出service中，pod不会重启；后一个失败pod会直接重启.
    默认情况下pod的健康检查会在pod启动以后的120s以后进行（1.16之前）所以目前来说这个值尽量设置小一点。
    172.16.1.23 内网的一个DNS 可以用来做域名解析

### 环境资源配置
    sit环境里面 cpu 不会启用CPU配额限制，也就是如果设置了0.1CPU 运行时使用的资源是绝对不会超过这个值的

gitlab 的 ci/cd 的基础镜像？

sit -> prof -> uat -> pro 四种环境

helm 这个仓库回自己去调用marthon的接口 现在是人为调用marthon的接口

### 使用的是elk的日志平台
k8s_dashboard 也是可以查看到所有的日志的

### 分离config repo
    第一个部分是公共部分，spring cloud的全局部分 由现有的config repo管理
    第二部分是应用自身配置，这部分内容由大家自己管理
这样做的目的主要是为了控制git仓库的大小

### 