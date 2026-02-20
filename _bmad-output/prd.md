---
stepsCompleted: [1, 2, 3, 4, 7, 8, 9, 10]
workflowType: 'prd'
project_name: 'iMaotai'
user_name: 'Cc'
date: '2026-02-19'
---

# Product Requirements Document - iMaotai (Pivoted: Fixed-Sequence Mode)

**Author:** Cc
**Date:** 2026-02-19

## Executive Summary

iMaotai 是一款专为开发者设计的、基于**高精度坐标序列模拟**的安卓自动化抢购工具。为了追求极致的响应速度并降低硬件开销，本项目弃用了耗时较长的 OCR 方案，转而采用“录制+回放”的策略。通过预先设定 App 的固定位置及点击路径，配合**生理级行为混淆系统**（随机偏移、贝塞尔轨迹、压感模拟），实现在不依赖复杂视觉计算的前提下，以毫秒级速度完成抢购动作，同时最大程度规避自动化检测。

### What Makes This Special

- **毫秒级极速执行：** 移除 OCR 推理，点击动作即时触发，确保在抢购瞬间占据先机。
- **生理级行为隐蔽：** 即使是固定坐标，系统也会通过 `scipy` 算法引入微小的正态分布偏移和非线性轨迹，确保护航账号安全。
- **声明式路径配置：** 抢购流程通过 JSON 描述，包含点击坐标、随机延迟范围及防御等级。
- **环境自适应：** 依然支持 Webhook 异地通知，确保挂机状态透明。

## Project Classification

**Technical Type:** Developer Tool / Input Simulation Engine
**Domain:** Automation / Mobile Security
**Complexity:** Medium (Focused on stealth and precision)
**Project Context:** Greenfield - Pivoted from OCR

## Success Criteria

- **操作精准度：** 固定坐标点击的有效性需达到 100%（需保持 UI 环境静止）。
- **账号安全：** 通过生理级混淆算法，长期挂机不被判定为机器人。
- **时间成本：** 实现真正的“设定即忘”，每日准时自动执行。

## Product Scope (MVP)

- **核心执行引擎：** 读取 JSON 坐标序列并顺序执行。
- **生理级模拟系统：** L1-L2 防御（随机偏移、压力、轨迹）。
- **坐标录制助手：** 辅助获取 App 在特定屏幕下的像素坐标。
- **远程通知：** 结果回传至 Webhook。
