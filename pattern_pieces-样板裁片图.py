#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物兔胃部肿瘤术后康复衣 - 服装样板裁片图
展示所有独立裁片，含尺寸标注与面料说明
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc, FancyBboxPatch, Rectangle
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def draw_pattern_piece(ax, x_offset, y_offset, name, size_text, fabric_text, draw_func):
    """绘制单个裁片的通用框架"""
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'{name}\n{size_text}', fontsize=10, fontweight='bold')
    draw_func(ax, x_offset, y_offset)
    ax.text(0.5, -0.1, fabric_text, transform=ax.transAxes, ha='center', 
            fontsize=8, style='italic', color='darkblue')

def draw_ventral_body(ax, ox, oy):
    """腹侧主体裁片"""
    # 轮廓
    top_y = oy
    bottom_y = oy + 220
    top_half_w = 40
    bottom_half_w = 90
    
    x = [-top_half_w+ox, top_half_w+ox, bottom_half_w+ox, -bottom_half_w+ox, -top_half_w+ox]
    y = [top_y, top_y, bottom_y, bottom_y, top_y]
    ax.plot(x, y, 'k-', linewidth=1.5)
    
    # 底部圆角
    ax.add_patch(Arc((-bottom_half_w+20+ox, bottom_y-20), 40, 40, angle=0, theta1=90, theta2=180, color='k', linewidth=1.5))
    ax.add_patch(Arc((bottom_half_w-20+ox, bottom_y-20), 40, 40, angle=0, theta1=0, theta2=90, color='k', linewidth=1.5))
    
    # 前肢开孔
    ax.add_patch(Circle((-30+ox, oy+40), 17.5, fill=False, edgecolor='k', linewidth=1.2))
    ax.add_patch(Circle((30+ox, oy+40), 17.5, fill=False, edgecolor='k', linewidth=1.2))
    
    # 排泄开口
    excrete_top_y = oy + 190
    ax.add_patch(Arc((ox, excrete_top_y), 50, 60, angle=0, theta1=180, theta2=360, color='k', linewidth=1.2))
    ax.plot([-25+ox, -25+ox], [excrete_top_y, bottom_y], 'k-', linewidth=1.2)
    ax.plot([25+ox, 25+ox], [excrete_top_y, bottom_y], 'k-', linewidth=1.2)
    
    # 核心防护区对位标记
    ax.add_patch(FancyBboxPatch((-40+ox, oy+50), 80, 100,
                                boxstyle="round,pad=0,rounding_size=10",
                                fill=False, edgecolor='r', linewidth=1, linestyle=':'))
    
    # 缝份示意 (虚线外扩10mm)
    seam = 10
    ax.plot([-top_half_w-seam+ox, top_half_w+seam+ox], [top_y-seam, top_y-seam], 'k:', linewidth=0.5, alpha=0.5)
    
    # 尺寸标注
    ax.text(ox, oy-15, '80mm', ha='center', fontsize=7)
    ax.plot([-top_half_w+ox, top_half_w+ox], [oy-8, oy-8], 'k-', linewidth=0.5)
    ax.text(-bottom_half_w-15+ox, oy+110, '220mm', va='center', rotation=90, fontsize=7)

def draw_dorsal_body(ax, ox, oy):
    """背侧主体裁片"""
    top_y = oy
    bottom_y = oy + 220
    top_half_w = 50
    bottom_half_w = 80
    
    x = [-top_half_w+ox, top_half_w+ox, bottom_half_w+ox, -bottom_half_w+ox, -top_half_w+ox]
    y = [top_y, top_y, bottom_y, bottom_y, top_y]
    ax.plot(x, y, 'k-', linewidth=1.5)
    
    ax.add_patch(Arc((-bottom_half_w+15+ox, bottom_y-15), 30, 30, angle=0, theta1=90, theta2=180, color='k', linewidth=1.5))
    ax.add_patch(Arc((bottom_half_w-15+ox, bottom_y-15), 30, 30, angle=0, theta1=0, theta2=90, color='k', linewidth=1.5))
    
    # 肩带对位标记
    ax.plot([-30+ox, -10+ox], [oy, oy], 'r:', linewidth=1)
    ax.plot([10+ox, 30+ox], [oy, oy], 'r:', linewidth=1)
    
    # 绑带对位标记
    ax.plot([-bottom_half_w-5+ox, -bottom_half_w+5+ox], [oy+110, oy+110], 'r:', linewidth=1)
    ax.plot([bottom_half_w-5+ox, bottom_half_w+5+ox], [oy+110, oy+110], 'r:', linewidth=1)
    
    # 尺寸标注
    ax.text(ox, oy-15, '100mm', ha='center', fontsize=7)
    ax.text(-bottom_half_w-15+ox, oy+110, '220mm', va='center', rotation=90, fontsize=7)

def draw_core_protection(ax, ox, oy):
    """核心防护区裁片"""
    w, h = 80, 100
    ax.add_patch(FancyBboxPatch((-w/2+ox, oy), w, h,
                                boxstyle="round,pad=0,rounding_size=10",
                                fill=False, edgecolor='k', linewidth=1.5))
    # 斜线填充表示复合面料
    for i in range(8):
        xi = -w/2 + 5 + i*10 + ox
        ax.plot([xi, xi+5], [oy, oy+h], 'k:', linewidth=0.5, alpha=0.6)
    
    # 窗口对位
    ax.add_patch(FancyBboxPatch((-35+ox, oy+10), 70, 80,
                                boxstyle="round,pad=0,rounding_size=8",
                                fill=False, edgecolor='r', linewidth=0.8, linestyle=':'))
    
    ax.text(ox, oy-10, '80 x 100mm', ha='center', fontsize=7)

def draw_window_flap(ax, ox, oy):
    """换药窗口翻盖裁片"""
    w, h = 70, 80
    ax.add_patch(FancyBboxPatch((-w/2+ox, oy), w, h,
                                boxstyle="round,pad=0,rounding_size=8",
                                fill=False, edgecolor='k', linewidth=1.5))
    # 暗扣位置标记
    for sx in [-25, 0, 25]:
        ax.plot(sx+ox, oy+10, 'ko', markersize=2)
        ax.plot(sx+ox, oy+70, 'ko', markersize=2)
    
    ax.text(ox, oy-10, '70 x 80mm', ha='center', fontsize=7)

def draw_shoulder_strap(ax, ox, oy):
    """肩带裁片 (x2)"""
    w, h = 20, 100
    ax.add_patch(Rectangle((-w/2+ox, oy), w, h, fill=False, edgecolor='k', linewidth=1.5))
    # 魔术贴区
    ax.add_patch(Rectangle((-w/2+ox, oy+70), w, 30, fill=True, facecolor='gray', alpha=0.3, hatch='///'))
    
    ax.text(ox, oy-10, '20 x 100mm  x2pcs', ha='center', fontsize=7)
    ax.text(ox, oy+85, 'Velcro', ha='center', fontsize=6, color='darkred')

def draw_waist_belt(ax, ox, oy):
    """腰腹绑带裁片 (x2)"""
    w, h = 25, 120
    ax.add_patch(Rectangle((-w/2+ox, oy), w, h, fill=False, edgecolor='k', linewidth=1.5))
    # 魔术贴区
    ax.add_patch(Rectangle((-w/2+ox, oy+90), w, 30, fill=True, facecolor='gray', alpha=0.3, hatch='///'))
    
    ax.text(ox, oy-10, '25 x 120mm  x2pcs', ha='center', fontsize=7)

def draw_binding_strip(ax, ox, oy):
    """包边条裁片"""
    w, h = 30, 200
    ax.add_patch(Rectangle((-w/2+ox, oy), w, h, fill=False, edgecolor='k', linewidth=1.5))
    # 45度斜裁示意
    for i in range(0, 200, 20):
        ax.plot([-w/2+ox, w/2+ox], [oy+i, oy+i+15], 'k:', linewidth=0.5, alpha=0.5)
    
    ax.text(ox, oy-10, '宽30mm, 总长1200mm\n(45° bias cut)', ha='center', fontsize=7)

def main():
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('宠物兔胃部肿瘤术后康复衣 - 服装样板裁片图\n(胃部肿瘤手术, S码, 缝份: 10mm, 单位: mm)',
                 fontsize=14, fontweight='bold', y=0.98)
    
    # 布局: 3行3列
    # 第1行: 腹侧主体、背侧主体、核心防护区
    # 第2行: 换药窗口、肩带、腰腹绑带
    # 第3行: 包边条 + 工艺说明
    
    # 1. 腹侧主体裁片
    ax1 = fig.add_subplot(3, 3, 1)
    ax1.set_xlim(-120, 120)
    ax1.set_ylim(-30, 250)
    ax1.invert_yaxis()
    draw_pattern_piece(ax1, 0, 0, '裁片1: 腹侧主体', '220mm高 x 80-180mm宽', 
                       '面料: 透气棉网眼布 (80-120g/㎡)', draw_ventral_body)
    
    # 2. 背侧主体裁片
    ax2 = fig.add_subplot(3, 3, 2)
    ax2.set_xlim(-110, 110)
    ax2.set_ylim(-30, 250)
    ax2.invert_yaxis()
    draw_pattern_piece(ax2, 0, 0, '裁片2: 背侧主体', '220mm高 x 100-160mm宽',
                       '面料: 透气棉网眼布 (80-120g/㎡)', draw_dorsal_body)
    
    # 3. 核心防护区裁片
    ax3 = fig.add_subplot(3, 3, 3)
    ax3.set_xlim(-60, 60)
    ax3.set_ylim(-20, 130)
    ax3.invert_yaxis()
    draw_pattern_piece(ax3, 0, 0, '裁片3: 核心防护区', '80 x 100mm',
                       '面料: 防咬透气复合面料\n(HDPE网格 + 亲肤内衬, 1.2mm)', 
                       draw_core_protection)
    
    # 4. 换药窗口翻盖
    ax4 = fig.add_subplot(3, 3, 4)
    ax4.set_xlim(-50, 50)
    ax4.set_ylim(-20, 110)
    ax4.invert_yaxis()
    draw_pattern_piece(ax4, 0, 0, '裁片4: 换药窗口翻盖', '70 x 80mm',
                       '面料: 同核心防护区\n(6颗按扣)', 
                       draw_window_flap)
    
    # 5. 肩带
    ax5 = fig.add_subplot(3, 3, 5)
    ax5.set_xlim(-30, 30)
    ax5.set_ylim(-20, 130)
    ax5.invert_yaxis()
    draw_pattern_piece(ax5, 0, 0, '裁片5: 肩带', '20 x 100mm (2条)',
                       '材料: 棉织带 + 魔术贴', 
                       draw_shoulder_strap)
    
    # 6. 腰腹绑带
    ax6 = fig.add_subplot(3, 3, 6)
    ax6.set_xlim(-35, 35)
    ax6.set_ylim(-20, 150)
    ax6.invert_yaxis()
    draw_pattern_piece(ax6, 0, 0, '裁片6: 腰腹绑带', '25 x 120mm (2条)',
                       '材料: 棉织带 + 魔术贴', 
                       draw_waist_belt)
    
    # 7. 包边条
    ax7 = fig.add_subplot(3, 3, 7)
    ax7.set_xlim(-40, 40)
    ax7.set_ylim(-30, 230)
    ax7.invert_yaxis()
    draw_pattern_piece(ax7, 0, 0, '裁片7: 包边条', '30mm wide',
                       '材料: 高强度尼龙\n(所有边缘防咬包边)', 
                       draw_binding_strip)
    
    # 8. 工艺说明区
    ax8 = fig.add_subplot(3, 3, (8, 9))
    ax8.axis('off')
    ax8.set_title('缝制工艺规范', fontsize=12, fontweight='bold')
    
    process_text = """
    1. 缝份: 所有接缝均为10mm, 包边处除外.
    
    2. 缝制顺序:
       - 步骤1: 预复合核心防护面料 (网格 + 内衬)
       - 步骤2: 将换药窗口翻盖缝至核心防护区 (仅上缘)
       - 步骤3: 将核心防护区固定至腹侧主体内侧
       - 步骤4: 缝合腹侧与背侧主体的侧缝
       - 步骤5: 对所有外缘、腿孔、排泄开口进行防咬包边
       - 步骤6: 将肩带和腰腹绑带缝至背侧主体
       - 步骤7: 在绑带末端固定魔术贴
    
    3. 特殊工艺:
       - 内侧采用平缝 (无凸起线迹), 避免皮肤刺激
       - 所有硬质部件 (按扣、插扣) 仅置于背侧
       - U型排泄开口, 加固包边
    
    4. 尺码放码 (等比例缩放):
       - XS: 70% (1-2kg 侏儒兔)
       - S:  100% (2-3.5kg 标准兔)
       - M:  130% (3.5-5kg 大型兔)
    
    5. 质量要求:
       - 无线头, 无毛边外露
       - 核心防护区须能承受兔切齿啃咬
       - 所有开口与兔体解剖结构精确对位
    """
    
    ax8.text(0.05, 0.95, process_text, transform=ax8.transAxes,
             fontsize=9, va='top', family='Microsoft YaHei',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    
    output_path = 'recovery_suit_pattern_pieces.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"样板裁片图已保存至: {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
