MERGE INTO birthday_info (
    id, recipient_name, birthday_date, hero_title, blessing_title, blessing_text,
    card_salutation, card_message, music_url
) KEY (id) VALUES (
    1, '廖思覃', '2026-08-18', '廖思覃，生日快乐', '给新一岁的你',
    '愿你的每一天，都有微小的惊喜在等着你。',
    '亲爱的廖思覃', '叮！按时长大！愿你新的一岁暴富暴美，快乐加倍！',
    '/Christina Perri - A Thousand Years.mp3'
);
