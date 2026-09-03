#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物兔胃部肿瘤术后康复衣 - 三视图绘制
生成腹侧主视图、背侧后视图、左侧视图
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Arc, FancyBboxPatch
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

def draw_ventral_view(ax):
    """腹侧主视图"""
    ax.set_title('腹侧主视图', fontsize=12, fontweight='bold', pad=10)
    ax.set_aspect('equal')
    ax.set_xlim(-110, 110)
    ax.set_ylim(-10, 240)
    ax.invert_yaxis()
    
    # 隐藏坐标轴
    ax.axis('off')
    
    # 1. 腹侧主体片外轮廓 - 上窄下宽梯形
    # 顶部宽度80mm, 底部宽度180mm, 高度220mm
    top_y = 0
    bottom_y = 220
    top_half_w = 40
    bottom_half_w = 90
    
    # 绘制主体轮廓
    body_x = [-top_half_w, top_half_w, bottom_half_w, -bottom_half_w, -top_half_w]
    body_y = [top_y, top_y, bottom_y, bottom_y, top_y]
    ax.plot(body_x, body_y, 'k-', linewidth=1.5)
    
    # 底部圆角
    bottom_left_arc = Arc((-bottom_half_w+20, bottom_y-20), 40, 40, angle=0, theta1=90, theta2=180, color='k', linewidth=1.5)
    bottom_right_arc = Arc((bottom_half_w-20, bottom_y-20), 40, 40, angle=0, theta1=0, theta2=90, color='k', linewidth=1.5)
    ax.add_patch(bottom_left_arc)
    ax.add_patch(bottom_right_arc)
    
    # 2. 前肢开孔 (左右对称)
    limb_circle_r = 17.5
    limb_y = 40
    left_limb_x = -30
    right_limb_x = 30
    
    left_limb = Circle((left_limb_x, limb_y), limb_circle_r, fill=False, edgecolor='k', linewidth=1.2)
    right_limb = Circle((right_limb_x, limb_y), limb_circle_r, fill=False, edgecolor='k', linewidth=1.2)
    ax.add_patch(left_limb)
    ax.add_patch(right_limb)
    
    # 3. 核心防护区 - 圆角矩形
    protect_x1, protect_x2 = -40, 40
    protect_y1, protect_y2 = 50, 150
    protect_rect = FancyBboxPatch((protect_x1, protect_y1), protect_x2-protect_x1, protect_y2-protect_y1,
                                  boxstyle="round,pad=0,rounding_size=10", 
                                  fill=False, edgecolor='k', linewidth=1.5, linestyle='--')
    ax.add_patch(protect_rect)
    # 填充斜线表示复合面料
    for x in np.linspace(protect_x1+5, protect_x2-5, 8):
        ax.plot([x, x+5], [protect_y1, protect_y2], 'k:', linewidth=0.5, alpha=0.5)
    
    # 4. 换药窗口翻盖
    window_x1, window_x2 = -35, 35
    window_y1, window_y2 = 60, 140
    window_rect = FancyBboxPatch((window_x1, window_y1), window_x2-window_x1, window_y2-window_y1,
                                 boxstyle="round,pad=0,rounding_size=8",
                                 fill=False, edgecolor='k', linewidth=1.2)
    ax.add_patch(window_rect)
    
    # 暗扣位置
    snap_positions = [(-25, 70), (0, 70), (25, 70), (-25, 130), (0, 130), (25, 130)]
    for sx, sy in snap_positions:
        ax.plot(sx, sy, 'ko', markersize=3)
    
    # 5. 排泄开口 - U型
    excrete_top_y = 190
    excrete_half_w = 25
    excrete_depth = 30
    # U型弧线
    excrete_arc = Arc((0, excrete_top_y), excrete_half_w*2, excrete_depth*2, angle=0, theta1=180, theta2=360, color='k', linewidth=1.2)
    ax.add_patch(excrete_arc)
    # 两侧竖线
    ax.plot([-excrete_half_w, -excrete_half_w], [excrete_top_y, bottom_y], 'k-', linewidth=1.2)
    ax.plot([excrete_half_w, excrete_half_w], [excrete_top_y, bottom_y], 'k-', linewidth=1.2)
    
    # 6. 防啃咬包边示意 (内偏移3mm)
    # 简化表示，在关键边缘标注
    
    
    # 引线标注（箭头尖→标注文字，加长引线确保清晰）
    arrow_kw = dict(arrowstyle='->', color='k', lw=1.2, connectionstyle='arc3,rad=0.15')
    # ① 腹侧主体片：指向身体轮廓边缘
    ax.annotate('①', xy=(56, 60), xytext=(95, 60), fontsize=9, fontweight='bold', arrowprops=arrow_kw)
    # ② 核心防护区：指向防护区内部
    ax.annotate('②', xy=(25, 130), xytext=(65, 155), fontsize=9, fontweight='bold', arrowprops=arrow_kw)
    # ③ 换药窗口翻盖：指向窗口中心
    ax.annotate('③', xy=(0, 100), xytext=(60, 70), fontsize=9, fontweight='bold', arrowprops=arrow_kw)
    # ④ 前肢开孔：指向左前肢孔中心
    ax.annotate('④', xy=(-30, 40), xytext=(-68, 30), fontsize=9, fontweight='bold', arrowprops=arrow_kw)
    # ⑤ 排泄开口：指向U型开口内部
    ax.annotate('⑤', xy=(0, 205), xytext=(35, 238), fontsize=9, fontweight='bold', arrowprops=arrow_kw)
    # ⑥ 防咬包边：指向身体右侧边缘
    ax.annotate('⑥', xy=(69, 145), xytext=(95, 145), fontsize=9, fontweight='bold', arrowprops=arrow_kw)
    
    # 尺寸标注
    # 总高度
    ax.plot([-100, -100], [0, 220], 'k-', linewidth=0.8)
    ax.plot([-103, -97], [0, 0], 'k-', linewidth=0.8)
    ax.plot([-103, -97], [220, 220], 'k-', linewidth=0.8)
    ax.text(-108, 110, '220mm', rotation=90, va='center', ha='right', fontsize=8)
    
    # 底部宽度
    ax.plot([-90, 90], [230, 230], 'k-', linewidth=0.8)
    ax.plot([-90, -90], [227, 233], 'k-', linewidth=0.8)
    ax.plot([90, 90], [227, 233], 'k-', linewidth=0.8)
    ax.text(0, 235, '180mm', ha='center', fontsize=8)

def draw_dorsal_view(ax):
    """背侧后视图"""
    ax.set_title('背侧后视图', fontsize=12, fontweight='bold', pad=10)
    ax.set_aspect('equal')
    ax.set_xlim(-130, 130)
    ax.set_ylim(-10, 240)
    ax.invert_yaxis()
    ax.axis('off')
    
    # 1. 背侧主体片
    top_y = 0
    bottom_y = 220
    top_half_w = 50
    bottom_half_w = 80
    
    body_x = [-top_half_w, top_half_w, bottom_half_w, -bottom_half_w, -top_half_w]
    body_y = [top_y, top_y, bottom_y, bottom_y, top_y]
    ax.plot(body_x, body_y, 'k-', linewidth=1.5)
    
    # 底部圆角
    bottom_left_arc = Arc((-bottom_half_w+15, bottom_y-15), 30, 30, angle=0, theta1=90, theta2=180, color='k', linewidth=1.5)
    bottom_right_arc = Arc((bottom_half_w-15, bottom_y-15), 30, 30, angle=0, theta1=0, theta2=90, color='k', linewidth=1.5)
    ax.add_patch(bottom_left_arc)
    ax.add_patch(bottom_right_arc)
    
    # 2. 可调肩带组 (左右两条)
    strap_width = 20
    strap_length = 80
    strap_y_start = 0
    
    # 左肩带
    left_strap_x = -20
    ax.plot([left_strap_x - strap_width/2, left_strap_x - strap_width/2], [strap_y_start, strap_y_start+strap_length], 'k-', linewidth=1.2)
    ax.plot([left_strap_x + strap_width/2, left_strap_x + strap_width/2], [strap_y_start, strap_y_start+strap_length], 'k-', linewidth=1.2)
    ax.plot([left_strap_x - strap_width/2, left_strap_x + strap_width/2], [strap_y_start+strap_length, strap_y_start+strap_length], 'k-', linewidth=1.2)
    
    # 右肩带
    right_strap_x = 20
    ax.plot([right_strap_x - strap_width/2, right_strap_x - strap_width/2], [strap_y_start, strap_y_start+strap_length], 'k-', linewidth=1.2)
    ax.plot([right_strap_x + strap_width/2, right_strap_x + strap_width/2], [strap_y_start, strap_y_start+strap_length], 'k-', linewidth=1.2)
    ax.plot([right_strap_x - strap_width/2, right_strap_x + strap_width/2], [strap_y_start+strap_length, strap_y_start+strap_length], 'k-', linewidth=1.2)
    
    # 肩带魔术贴区 (末端)
    velcro_length = 30
    ax.fill_between([left_strap_x-strap_width/2, left_strap_x+strap_width/2], 
                    strap_y_start+strap_length-velcro_length, strap_y_start+strap_length, 
                    color='gray', alpha=0.3, hatch='///')
    ax.fill_between([right_strap_x-strap_width/2, right_strap_x+strap_width/2], 
                    strap_y_start+strap_length-velcro_length, strap_y_start+strap_length, 
                    color='gray', alpha=0.3, hatch='///')
    
    # 3. 腰腹绑带组
    belt_width = 25
    belt_length = 40  # 单侧伸出长度
    belt_y = 110
    
    # 左绑带
    ax.plot([-bottom_half_w, -bottom_half_w-belt_length], [belt_y-belt_width/2, belt_y-belt_width/2], 'k-', linewidth=1.2)
    ax.plot([-bottom_half_w, -bottom_half_w-belt_length], [belt_y+belt_width/2, belt_y+belt_width/2], 'k-', linewidth=1.2)
    ax.plot([-bottom_half_w-belt_length, -bottom_half_w-belt_length], [belt_y-belt_width/2, belt_y+belt_width/2], 'k-', linewidth=1.2)
    
    # 右绑带
    ax.plot([bottom_half_w, bottom_half_w+belt_length], [belt_y-belt_width/2, belt_y-belt_width/2], 'k-', linewidth=1.2)
    ax.plot([bottom_half_w, bottom_half_w+belt_length], [belt_y+belt_width/2, belt_y+belt_width/2], 'k-', linewidth=1.2)
    ax.plot([bottom_half_w+belt_length, bottom_half_w+belt_length], [belt_y-belt_width/2, belt_y+belt_width/2], 'k-', linewidth=1.2)
    
    # 绑带魔术贴区
    ax.fill_between([-bottom_half_w-belt_length+15, -bottom_half_w-belt_length],
                    belt_y-belt_width/2, belt_y+belt_width/2, color='gray', alpha=0.3, hatch='///')
    ax.fill_between([bottom_half_w+belt_length-15, bottom_half_w+belt_length],
                    belt_y-belt_width/2, belt_y+belt_width/2, color='gray', alpha=0.3, hatch='///')
    
    # 4. 肩带固定区、绑带贴合区示意
    ax.text(0, 25, '⑩ 肩带固定区', ha='center', fontsize=8, style='italic')
    ax.text(0, 110, '(11) 绑带贴合区', ha='center', fontsize=8, style='italic')
    
    # 标注编号（箭头尖→标注文字，加长引线确保清晰）
    arrow_kw = dict(arrowstyle='->', color='k', lw=1.2, connectionstyle='arc3,rad=0.15')
    # ⑦ 背侧主体片：指向身体右侧轮廓
    ax.annotate('⑦', xy=(58, 80), xytext=(95, 75), fontsize=9, fontweight='bold', arrowprops=arrow_kw)
    # ⑧ 可调肩带组：指向肩带魔术贴区域
    ax.annotate('⑧', xy=(0, 55), xytext=(45, 20), fontsize=9, fontweight='bold', arrowprops=arrow_kw)
    # ⑨ 腰腹绑带组：指向右侧绑带中部
    ax.annotate('⑨', xy=(100, 110), xytext=(122, 95), fontsize=9, fontweight='bold', arrowprops=arrow_kw)
    
    # 尺寸标注
    ax.plot([-120, -120], [0, 220], 'k-', linewidth=0.8)
    ax.text(-125, 110, '220mm', rotation=90, va='center', ha='right', fontsize=8)

def draw_side_view(ax):
    """左侧视图"""
    ax.set_title('左侧视图', fontsize=12, fontweight='bold', pad=10)
    ax.set_aspect('equal')
    ax.set_xlim(-20, 100)
    ax.set_ylim(-10, 240)
    ax.invert_yaxis()
    ax.axis('off')
    
    # 侧面轮廓 - 腹部外凸10mm体现宽松减压
    # 前侧(左)、后侧(右)
    front_x = 20
    back_x = 80
    top_y = 0
    bottom_y = 220
    
    # 腹部凸出曲线
    belly_bulge = 10  # 腹部外凸余量
    belly_mid_y = 120
    
    # 绘制侧面轮廓
    # 背部直线
    ax.plot([back_x, back_x], [top_y, bottom_y], 'k-', linewidth=1.5)
    # 腹部曲线 (凸出)
    belly_x_points = [front_x, front_x+belly_bulge*0.3, front_x+belly_bulge, front_x+belly_bulge*0.5, front_x]
    belly_y_points = [top_y, belly_mid_y*0.5, belly_mid_y, belly_mid_y*1.5, bottom_y]
    
    from scipy.interpolate import make_interp_spline
    y_new = np.linspace(top_y, bottom_y, 100)
    spl = make_interp_spline(belly_y_points, belly_x_points, k=3)
    x_smooth = spl(y_new)
    ax.plot(x_smooth, y_new, 'k-', linewidth=1.5)
    
    # 上下连接线
    ax.plot([front_x, back_x], [top_y, top_y], 'k-', linewidth=1.5)
    ax.plot([front_x, back_x], [bottom_y, bottom_y], 'k-', linewidth=1.5)
    
    # 核心防护区侧面位置
    protect_y1, protect_y2 = 50, 150
    ax.plot([front_x+belly_bulge*0.5, back_x], [protect_y1, protect_y1], 'k--', linewidth=0.8)
    ax.plot([front_x+belly_bulge*0.7, back_x], [protect_y2, protect_y2], 'k--', linewidth=0.8)
    ax.text(50, 100, '核心防护区\n（复合面料）', ha='center', fontsize=8, style='italic')
    
    # 标注腹部舒张余量
    ax.annotate('', xy=(front_x, belly_mid_y), xytext=(front_x+belly_bulge, belly_mid_y),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1))
    ax.text(front_x+belly_bulge/2, belly_mid_y-8, '10mm\n腹部\n舒张余量', ha='center', fontsize=7, fontweight='bold')
    
    # 前肢开孔侧面位置
    limb_y = 40
    ax.plot([front_x-5, front_x+5], [limb_y, limb_y], 'k-', linewidth=1)
    ax.text(front_x-8, limb_y, '前肢开孔', ha='right', va='center', fontsize=8)
    
    # 肩带位置
    ax.plot([back_x-5, back_x+5], [40, 40], 'k-', linewidth=1)
    ax.text(back_x+8, 40, '肩带', ha='left', va='center', fontsize=8)
    
    # 腰腹绑带位置
    ax.plot([back_x-5, back_x+5], [110, 110], 'k-', linewidth=1)
    ax.text(back_x+8, 110, '腰腹绑带', ha='left', va='center', fontsize=8)
    
    # 复合面料厚度示意
    ax.annotate('', xy=(front_x+belly_bulge-1.2, 100), xytext=(front_x+belly_bulge, 100),
                arrowprops=dict(arrowstyle='<->', color='k', lw=0.8))
    ax.text(front_x+belly_bulge+2, 100, '1.2mm', fontsize=7, va='center')

def main():
    # 创建画布 - 三视图横向排列
    fig, axes = plt.subplots(1, 3, figsize=(18, 10))
    fig.suptitle('宠物兔胃部肿瘤术后康复衣 - 三视图（S码，单位：mm）', 
                 fontsize=14, fontweight='bold', y=0.98)
    
    draw_ventral_view(axes[0])
    draw_dorsal_view(axes[1])
    draw_side_view(axes[2])
    
    # 添加图例说明
    legend_text = [
        '图例说明：',
        '① 腹侧主体片',
        '② 核心防护区（防咬透气面料）',
        '③ 换药窗口翻盖',
        '④ 前肢开孔',
        '⑤ 排泄开口',
        '⑥ 防咬包边',
        '⑦ 背侧主体片',
        '⑧ 可调肩带组',
        '⑨ 腰腹绑带组',
        '⑩ 肩带固定区',
        '(11) 绑带贴合区',
    ]
    
    fig.text(0.02, 0.02, '\n'.join(legend_text), fontsize=9, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout(rect=[0, 0.12, 1, 0.95])
    
    # 保存图片
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'recovery_suit_three_views.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"三视图已保存至: {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
