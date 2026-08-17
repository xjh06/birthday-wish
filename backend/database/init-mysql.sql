-- 生产环境建议先执行 schema.sql 创建表，再执行本脚本写入初始配置。
INSERT INTO birthday_info (
    id, recipient_name, birthday_date, hero_title, blessing_title, blessing_text,
    card_salutation, card_message, music_url
) VALUES (
    1, '廖思覃', '2026-08-17', '廖思覃，生日快乐', '给新一岁的你',
    '愿你的每一天，都有微小的惊喜在等着你。',
    '亲爱的廖思覃', '叮！按时长大！愿你新的一岁暴富暴美，快乐加倍！',
    '/Christina Perri - A Thousand Years.mp3'
)
ON DUPLICATE KEY UPDATE
    recipient_name = VALUES(recipient_name),
    birthday_date = VALUES(birthday_date),
    hero_title = VALUES(hero_title),
    blessing_title = VALUES(blessing_title),
    blessing_text = VALUES(blessing_text),
    card_salutation = VALUES(card_salutation),
    card_message = VALUES(card_message),
    music_url = VALUES(music_url);
