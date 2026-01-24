SELECT tablename 
FROM pg_tables 
WHERE tablename LIKE 'edu_%';

-- xóa tất
DELETE FROM edu_session_attendee_rel;
DELETE FROM edu_session;
DELETE FROM edu_course;
DELETE FROM edu_classroom;
DELETE FROM edu_subject;

-- kiểm tra bảng trong module contacts
-- 1. Xem tất cả dữ liệu trong bảng Contacts (Đối tác/Liên hệ)
SELECT * FROM res_partner;

-- 2. Xem danh sách chỉ lấy Tên và Email cho gọn
SELECT id, name, email, phone FROM res_partner;

-- 3. Kiểm tra xem có cột custom (is_student, is_instructor) không
-- (Chỉ chạy được nếu module edu_management đã được cài và update)
SELECT id, name, is_student, is_instructor FROM res_partner;

-- 4. Lấy riêng danh sách Giảng viên
SELECT * FROM res_partner WHERE is_instructor = true;

-- 5. Lấy riêng danh sách Học viên
SELECT * FROM res_partner WHERE is_student = true;


INSERT INTO res_partner (
    name, 
    email, 
    email_normalized, 
    phone, 
    comment,
    is_instructor, 
    is_student, 
    edu_role, -- Thêm cột này
    active, 
    lang, 
    tz, 
    type,
    create_date,
    write_date
) VALUES 
('Trần Văn Minh', 'tranvanminh.student@gmail.com', 'tranvanminh.student@gmail.com', '+84 901 234 567', 'Học viên khóa cơ bản', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Lê Thị Hạnh', 'lethihanh.student@gmail.com', 'lethihanh.student@gmail.com', '+84 912 345 678', 'Đăng ký qua website', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Phạm Đức Thắng', 'phamducthang.student@gmail.com', 'phamducthang.student@gmail.com', '+84 987 654 321', 'Quan tâm khóa lập trình', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Hoàng Thị Lan', 'hoangthilan.student@gmail.com', 'hoangthilan.student@gmail.com', '+84 934 567 890', 'Sinh viên năm cuối', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Vũ Văn Nam', 'vuvanam.student@gmail.com', 'vuvanam.student@gmail.com', '+84 945 678 901', 'Đã đóng học phí', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Đặng Thị Mai', 'dangthimai.student@gmail.com', 'dangthimai.student@gmail.com', '+84 856 789 012', 'Học viên tiềm năng', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Bùi Văn Tuấn', 'buivantuan.student@gmail.com', 'buivantuan.student@gmail.com', '+84 867 890 123', 'Cần tư vấn thêm', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Đỗ Thị Thu', 'dothithu.student@gmail.com', 'dothithu.student@gmail.com', '+84 888 901 234', 'Đạt học bổng', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Hồ Văn Huy', 'hovanhuy.student@gmail.com', 'hovanhuy.student@gmail.com', '+84 899 012 345', 'Chuyển lớp từ khóa trước', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Ngô Thị Ngọc', 'ngothingoc.student@gmail.com', 'ngothingoc.student@gmail.com', '+84 324 567 891', 'Đăng ký nhóm 3 người', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Dương Văn Hùng', 'duongvanhung.student@gmail.com', 'duongvanhung.student@gmail.com', '+84 335 678 902', 'Xin học bù', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Lý Thị Phương', 'lythiphuong.student@gmail.com', 'lythiphuong.student@gmail.com', '+84 346 789 013', 'Học viên xuất sắc', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Nguyễn Đức Anh', 'nguyenducanh.student@gmail.com', 'nguyenducanh.student@gmail.com', '+84 357 890 124', 'Lớp buổi tối', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Trần Thị Thanh', 'tranthithanh.student@gmail.com', 'tranthithanh.student@gmail.com', '+84 368 901 235', 'Lớp cuối tuần', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Lê Văn Long', 'levanlong.student@gmail.com', 'levanlong.student@gmail.com', '+84 379 012 346', 'Đã có laptop', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Phạm Thị Tuyết', 'phamthituyet.student@gmail.com', 'phamthituyet.student@gmail.com', '+84 381 123 457', 'Cần hỗ trợ cài đặt', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Hoàng Văn Hải', 'hoangvanhai.student@gmail.com', 'hoangvanhai.student@gmail.com', '+84 392 234 568', 'Sinh viên IT', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Vũ Thị Hương', 'vuthihuong.student@gmail.com', 'vuthihuong.student@gmail.com', '+84 703 345 679', 'Người đi làm', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Võ Văn Kiệt', 'vovankiet.student@gmail.com', 'vovankiet.student@gmail.com', '+84 764 456 780', 'Học viên cũ quay lại', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW()),
('Đặng Thị Yến', 'dangthiyen.student@gmail.com', 'dangthiyen.student@gmail.com', '+84 775 567 891', 'Đăng ký sớm', false, true, 'student', true, 'en_US', 'Asia/Ho_Chi_Minh', 'contact', NOW(), NOW());

-- tạo môn học
INSERT INTO edu_subject (
    name, 
    code, 
    description, 
    active, 
    create_uid, 
    write_uid, 
    create_date, 
    write_date
) VALUES 
('Lập trình Python cơ bản', 'SJ0001', 'Nhập môn lập trình với ngôn ngữ Python', true, 1, 1, NOW(), NOW()),
('Lập trình Web Frontend', 'SJ0002', 'Xây dựng giao diện web với HTML, CSS, JS', true, 1, 1, NOW(), NOW()),
('Lập trình Web Backend', 'SJ0003', 'Phát triển server-side với NodeJS/Django', true, 1, 1, NOW(), NOW()),
('Cơ sở dữ liệu SQL', 'SJ0004', 'Thiết kế và truy vấn database chuẩn SQL', true, 1, 1, NOW(), NOW()),
('Phân tích dữ liệu (Data Analysis)', 'SJ0005', 'Phân tích số liệu kinh doanh với Python/Excel', true, 1, 1, NOW(), NOW()),
('Thiết kế đồ họa Photoshop', 'SJ0006', 'Chỉnh sửa ảnh chuyên nghiệp', true, 1, 1, NOW(), NOW()),
('Tiếng Anh giao tiếp', 'SJ0007', 'Tiếng Anh cho người đi làm', true, 1, 1, NOW(), NOW()),
('Digital Marketing', 'SJ0008', 'Tiếp thị số trên nền tảng Facebook/Google', true, 1, 1, NOW(), NOW()),
('Quản trị nhân sự', 'SJ0009', 'Kỹ năng tuyển dụng và quản lý nhân sự', true, 1, 1, NOW(), NOW()),
('Kỹ năng mềm', 'SJ0010', 'Thuyết trình, làm việc nhóm, quản lý thời gian', true, 1, 1, NOW(), NOW());


-- tạo phòng học
INSERT INTO edu_classroom (
    name, 
    location, 
    capacity, 
    active, 
    create_uid, 
    write_uid, 
    create_date, 
    write_date
) VALUES 
('Phòng 101', 'Cơ sở 1 - Tầng 1', 30, true, 1, 1, NOW(), NOW()),
('Phòng 102', 'Cơ sở 1 - Tầng 1', 30, true, 1, 1, NOW(), NOW()),
('Phòng 201 (Lab)', 'Cơ sở 1 - Tầng 2', 25, true, 1, 1, NOW(), NOW()),
('Phòng 202 (Lab)', 'Cơ sở 1 - Tầng 2', 25, true, 1, 1, NOW(), NOW()),
('Phòng Hội trường A', 'Cơ sở 1 - Tầng 3', 100, true, 1, 1, NOW(), NOW()),
('Phòng 301', 'Cơ sở 2 - Tầng 3', 40, true, 1, 1, NOW(), NOW()),
('Phòng 302', 'Cơ sở 2 - Tầng 3', 35, true, 1, 1, NOW(), NOW()),
('Phòng 401 (VIP)', 'Cơ sở 2 - Tầng 4', 15, true, 1, 1, NOW(), NOW()),
('Phòng 402', 'Cơ sở 2 - Tầng 4', 20, true, 1, 1, NOW(), NOW()),
('Thư viện', 'Cơ sở 2 - Tầng 5', 50, true, 1, 1, NOW(), NOW());




