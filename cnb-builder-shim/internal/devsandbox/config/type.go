package config

// 源码获取方式
const (
	HTTP   = "HTTP"
	BKREPO = "BKREPO"
	GIT    = "GIT"
)

// SourceCodeConfig 源码配置
type SourceCodeConfig struct {
	// 源码获取方式
	SourceFetchMethod string
	// 源码地址
	SourceGetUrl string
	// Git 仓库版本
	GitRevision string
	// 工作目录
	Workspace string
}

// Config  全局配置
type Config struct {
	// 源码配置
	SourceCode SourceCodeConfig
	// ...
}
