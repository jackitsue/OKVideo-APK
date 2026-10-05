# OKVideo-APK

此專案用於對使用者自行提供且有權修改的 Android APK 進行重新封裝，目標是在影片詳情/集數操作中接上既有下載功能。

## 目標
- 保留原有播放流程
- 連接既有 DownloadActivity / Media3 下載元件
- 一般 MP4 / 可直接存取的 HLS(M3U8) 下載
- 不加入 DRM、付費內容保護或存取控制繞過
- 由 GitHub Actions 自動完成反編譯、重建、zipalign、簽章與 Artifact

## 使用方式
1. 將原始 APK 放到 `input/OKVideo-original.apk`
2. 推送後由 `.github/workflows/build-apk.yml` 執行
3. 成功後於 Actions Artifacts 下載重建 APK

> 注意：第三方 APK 重新簽章後通常無法直接覆蓋原版安裝。