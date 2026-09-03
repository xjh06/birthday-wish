#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物兔胃部肿瘤术后康复衣 - 术后护理使用流程图
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon
import platform
import os
import numpy as np

_system = platform.system()
if _system == 'Windows':
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
elif _system == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['Heiti SC', 'PingFang SC', 'STHeiti']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'Noto Sans SC']
plt.rcParams['axes.unicode_minus'] = False

def draw_process_box(ax, x, y, width, height, text, box_type='process'):
    """绘制流程框"""
    if box_type == 'start_end':
        # 起止框 - 圆角更大
        box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                             boxstyle="round,pad=0,rounding_size=15",
                             facecolor='#E8F4FD', edgecolor='#2C5F8D', linewidth=1.5)
    elif box_type == 'decision':
        # 决策框 - 菱形 (用多边形近似)
        points = [
            (x, y + height/2),
            (x + width/2, y),
            (x, y - height/2),
            (x - width/2, y)
        ]
        box = Polygon(points, facecolor='#FFF3CD', edgecolor='#856404', linewidth=1.5)
    else:
        # 普通流程框
        box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                             boxstyle="round,pad=0,rounding_size=5",
                             facecolor='#D4EDDA', edgecolor='#155724', linewidth=1.2)
    
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=10.5, fontweight='bold',
            wrap=True)
    return box

def draw_arrow(ax, x1, y1, x2, y2, label='', label_pos='center'):
    """绘制箭头"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle='->', color='#333', linewidth=1.2,
                            mutation_scale=22)
    ax.add_patch(arrow)
    
    if label:
        if label_pos == 'center':
            lx = (x1 + x2) / 2
            ly = (y1 + y2) / 2
        else:
            lx = x1
            ly = y1
        ax.text(lx, ly, label, fontsize=9, color='#222', ha='center', va='center',
                bbox=dict(facecolor='white', edgecolor='#ccc', pad=2))

def main():
    fig, ax = plt.subplots(figsize=(16, 20))
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 200)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.set_title('宠物兔胃部肿瘤术后康复衣\n术后护理使用流程图',
                 fontsize=14, fontweight='bold', pad=20)

    cx = 70
    lx = 22
    rx = 118
    box_w = 28
    box_h = 10
    step = 18

    current_y = 180

    draw_process_box(ax, cx, current_y, box_w, box_h, '开始\n术后穿戴准备', 'start_end')
    draw_arrow(ax, cx, current_y - 6, cx, current_y - 12)
    current_y -= step

    draw_process_box(ax, cx, current_y, box_w, box_h, '步骤1：选择尺寸\n匹配兔子体重与体型测量')
    draw_arrow(ax, cx, current_y - 6, cx, current_y - 12)
    current_y -= step

    draw_process_box(ax, cx, current_y, box_w, box_h, '步骤2：穿入前肢\n通过腿部开口')
    draw_arrow(ax, cx, current_y - 6, cx, current_y - 12)
    current_y -= step

    draw_process_box(ax, cx, current_y, box_w, box_h, '步骤3：调整固定肩带\n固定于背部')
    draw_arrow(ax, cx, current_y - 6, cx, current_y - 12)
    current_y -= step

    draw_process_box(ax, cx, current_y, box_w, box_h, '步骤4：系紧腰部绑带\n预留5-15mm腹部空隙')
    draw_arrow(ax, cx, current_y - 6, cx, current_y - 12)
    current_y -= step

    draw_process_box(ax, cx, current_y, box_w, box_h, '步骤5：检查覆盖\n确认上腹部完全遮盖')
    draw_arrow(ax, cx, current_y - 6, cx, current_y - 12)
    current_y -= step

    draw_process_box(ax, cx, current_y, box_w+4, box_h+2, '是否需要\n换药处理？', 'decision')
    decision_y = current_y

    # Right branch: Normal protection mode (no dressing change needed)
    draw_process_box(ax, rx, decision_y-2, 32, box_h+6, '正常防护模式：\n• 防啃咬伤口保护\n• 分区透气\n• 正常进食与食粪行为')
    arrow_right = FancyArrowPatch((cx+16, decision_y), (rx-15, decision_y-2),
                                  arrowstyle='->', color='#333', linewidth=1.5, mutation_scale=22)
    ax.add_patch(arrow_right)
    ax.text((cx+16+rx-15)/2, (2*decision_y-2)/2, '无需换药', fontsize=9, color='#222',
            ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='#ccc', pad=2))

    # Left branch: Wound care
    draw_process_box(ax, lx, decision_y-14, 32, box_h+1, '打开换药窗口\n无需取下整件康复衣')
    draw_arrow(ax, cx-16, decision_y, lx+15, decision_y-14, '伤口检查/\n更换敷料')

    draw_process_box(ax, lx, decision_y-28, 32, box_h+1, '清洁消毒伤口\n观察愈合情况')
    draw_arrow(ax, lx, decision_y-20, lx, decision_y-24)

    draw_process_box(ax, lx, decision_y-42, 32, box_h+1, '闭合并固定窗口\n扣好所有按扣')
    draw_arrow(ax, lx, decision_y-33, lx, decision_y-38)

    # Return from left branch: curved arrow going right and down, then up
    arrow_return = FancyArrowPatch((lx+15, decision_y-42), (rx-15, decision_y-2),
                                   arrowstyle='->', color='#333', linewidth=1.5,
                                   mutation_scale=22, connectionstyle='arc3,rad=-0.35')
    ax.add_patch(arrow_return)
    # Exact Bezier midpoint using matplotlib Arc3 formula
    x1, y1 = lx+15, decision_y-42
    x2, y2 = rx-15, decision_y-2
    cx_mid = (x1 + x2) * 0.5
    cy_mid = (y1 + y2) * 0.5
    dx = x2 - x1
    dy = y2 - y1
    d = np.linalg.norm(np.array([dx, dy]))
    cx_mid += -dy * (-0.35) / d
    cy_mid += dx * (-0.35) / d
    cp1x = x1 + 2.0 * (cx_mid - x1) / 3.0
    cp1y = y1 + 2.0 * (cy_mid - y1) / 3.0
    cp2x = x2 + 2.0 * (cx_mid - x2) / 3.0
    cp2y = y2 + 2.0 * (cy_mid - y2) / 3.0
    # Cubic Bezier at t=0.5
    t = 0.5
    arc_midx = (1-t)**3*x1 + 3*(1-t)**2*t*cp1x + 3*(1-t)*t**2*cp2x + t**3*x2
    arc_midy = (1-t)**3*y1 + 3*(1-t)**2*t*cp1y + 3*(1-t)*t**2*cp2y + t**3*y2
    ax.text(arc_midx, arc_midy, '返回正常防护', fontsize=9, color='#222',
            ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='#ccc', pad=2))

    # Decision 2: Wound fully healed?
    current_y = decision_y - 60
    draw_process_box(ax, cx, current_y, box_w+4, box_h+2, '伤口已\n完全愈合？', 'decision')
    heal_y = current_y

    # From right branch down to healed decision
    draw_arrow(ax, rx, decision_y-8, rx, heal_y + 5, '持续防护观察中')
    draw_arrow(ax, rx-15, heal_y, cx+16, heal_y, '检查愈合状况')

    # NO loop: red arrow from healed diamond back to decision diamond (left edges)
    arrow_loop = FancyArrowPatch((cx-16, heal_y), (cx-16, decision_y),
                                 arrowstyle='->', color='#e74c3c', linewidth=2.0,
                                 mutation_scale=24, connectionstyle='arc3,rad=-0.5')
    ax.add_patch(arrow_loop)
    ax.text(cx-16+8, (heal_y+decision_y)/2, '否（伤口未愈合）',
            fontsize=9, color='#c0392b', fontweight='bold', ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='#c0392b', boxstyle='round,pad=0.3'))

    # End
    current_y -= 18
    draw_process_box(ax, cx, current_y, box_w, box_h, '结束\n康复完成，取下康复衣', 'start_end')
    draw_arrow(ax, cx, heal_y - 5, cx, current_y + 5, '是（已愈合）')

    # Legend with red arrow explanation
    legend_elements = [
        mpatches.Patch(facecolor='#E8F4FD', edgecolor='#2C5F8D', label='开始 / 结束'),
        mpatches.Patch(facecolor='#D4EDDA', edgecolor='#155724', label='流程步骤'),
        mpatches.Patch(facecolor='#FFF3CD', edgecolor='#856404', label='决策判断'),
        mpatches.Patch(facecolor='#ffeaea', edgecolor='#e74c3c', label='红色箭头：伤口未愈合，继续护理'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9, title='图例')

    # Bottom note
    ax.text(5, 5, 
            '注意：本康复衣不限制颈部活动，允许兔子正常进行食粪行为、\n进食和饮水，这对术后胃肠道恢复至关重要。',
            ha='left', fontsize=8, style='italic', color='#666')

    plt.tight_layout()

    output_path = os.path.join(os.getcwd(), 'recovery_suit_flowchart.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"流程图已保存至: {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
