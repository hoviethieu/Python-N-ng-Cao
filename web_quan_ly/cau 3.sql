DROP TABLE IF EXISTS danhsach;
-- Tạo bảng danhsach
CREATE TABLE danhsach (
    id SERIAL PRIMARY KEY,
    hoten VARCHAR(100),
    diachi VARCHAR(200)
);

-- Chèn dữ liệu mẫu
INSERT INTO danhsach (hoten, diachi) VALUES
('Nguyen Van A', '123 Le Loi, HCM'),
('Tran Thi B', '456 Nguyen Hue, HN');
SELECT setval('danhsach_id_seq', (SELECT MAX(id) FROM danhsach));
