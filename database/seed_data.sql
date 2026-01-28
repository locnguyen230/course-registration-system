INSERT INTO User (userID, userName, password, role, status) VALUES
('11111111-1111-1111-1111-111111111111', 'sv_it_01', '$2b$12$RIXJ/eHP6wVVMkD7.OKRw.arnzxK5o37A3xyJyNnSnY4sibcGbtxa', 'STUDENT', 'ACTIVE'),
('22222222-2222-2222-2222-222222222222', 'sv_lg_01', '$2b$12$mnCgr4PC5eDz2J8Uckpb0.dwy3sKnpLumLAg0unetP0SEY3OKxaCK', 'STUDENT', 'ACTIVE'),
('33333333-3333-3333-3333-333333333333', 'sv_it_02', '$2b$12$8AvJ7ydzEym2g0GVxxki3u994D3LlnTaiDvoRx2crcFywk3wpqGFu', 'STUDENT', 'ACTIVE'),
('44444444-4444-4444-4444-444444444444', 'gv_it_01', '$2b$12$Iz3kmLdBUdZQv2q0rJAwh.sXvTez2ZCIq6Jv.XKdPNqtg5A0zfcHy', 'INSTRUCTOR', 'ACTIVE'),
('55555555-5555-5555-5555-555555555555', 'gv_lg_01', '$2b$12$nW3W84BiQi7kC1aVmfN7L.yB8iLkBkWJElm5gKQ72wBODguDEL8dO', 'INSTRUCTOR', 'ACTIVE'),
('66666666-6666-6666-6666-666666666666', 'admin_01', '$2b$12$wtOtdgqIg.Mc7tpIKjnjxOtE4mjvQhTBkCONROabSacx3l5BXACK2', 'ADMIN', 'ACTIVE');

-- STUDENT
INSERT INTO Student (studentID, fullName, email, major, yearLevel, academicStatus, userID) VALUES
('202501000001', 'Nguyễn Văn A', 'a@sv.edu.vn', 'Công nghệ thông tin', 2, 'ENROLLED', '11111111-1111-1111-1111-111111111111'),
('202502000001', 'Trần Thị B', 'b@sv.edu.vn', 'Logistics', 3, 'ENROLLED', '22222222-2222-2222-2222-222222222222'),
('202501000002', 'Lê Văn C', 'c@sv.edu.vn', 'Công nghệ thông tin', 1, 'ENROLLED', '33333333-3333-3333-3333-333333333333');

-- INSTRUCTOR
INSERT INTO Instructor (instructorID, fullName, department, userID) VALUES
('GVIT0001', 'Nguyễn Anh Tuấn', 'CNTT', '44444444-4444-4444-4444-444444444444'),
('GVLG0001', 'Trần Bình Minh', 'Logistics', '55555555-5555-5555-5555-555555555555');

-- ADMINISTRATION
INSERT INTO Administration (adminID, fullName, userID) VALUES
('AD0001', 'Lê Thị Hoa', '66666666-6666-6666-6666-666666666666');

-- ACADEMIC CONFIGGURATION
INSERT INTO AcademicConfiguration (configID, academicYear, semester, policies, adminID) VALUES
('CFG-HK1-2025', '2025-2026', 'HK1-2025',
 'Sinh viên được đăng ký tối đa 18 tín chỉ và phải hoàn thành môn học tiên quyết',
 'AD0001');

-- REGISTRATION BATCH
INSERT INTO RegistrationBatch (batchID, semester, startTime, endTime, eligibleYearLevel, adminID) VALUES
('125IT1', 'HK1-2025', '2025-01-05 08:00:00', '2025-01-10 23:59:59', 2, 'AD0001'),
('125IT2', 'HK1-2025', '2025-01-11 08:00:00', '2025-01-15 23:59:59', 1, 'AD0001'),
('125LG1', 'HK1-2025', '2025-01-06 08:00:00', '2025-01-12 23:59:59', 2, 'AD0001');

-- COURSE
INSERT INTO Course (courseID, courseName, credits, description) VALUES
('IT101', 'Nhập môn Công nghệ thông tin', 3, 'Tổng quan CNTT'),
('IT201', 'Lập trình hướng đối tượng', 3, 'OOP'),
('IT301', 'Phân tích thiết kế phần mềm', 3, 'UML và phân tích'),
('IT401', 'Công nghệ phần mềm', 3, 'Quy trình phát triển phần mềm'),

('LG101', 'Nhập môn Logistics', 3, 'Tổng quan logistics'),
('LG201', 'Quản lý chuỗi cung ứng', 3, 'Supply Chain Management');

-- COURSE PREREQUISITES
INSERT INTO CoursePrerequisites (prerequisiteID, courseID) VALUES
('IT101', 'IT201'),
('IT201', 'IT301'),
('IT101', 'IT301'),
('IT301', 'IT401');

-- COURSE SECTION
INSERT INTO CourseSection (sectionID, sectionCode, semester, capacity, enrolledCount, schedule, courseID, instructorID) VALUES
('SEC-IT101-01', 'IT101.01', 'HK1-2025', 40, 38, 'Mon 08:00-10:00', 'IT101', 'GVIT0001'),
('SEC-IT201-01', 'IT201.01', 'HK1-2025', 30, 30, 'Tue 10:00-12:00', 'IT201', 'GVIT0001'),
('SEC-IT301-01', 'IT301.01', 'HK1-2025', 25, 20, 'Wed 13:00-15:00', 'IT301', 'GVIT0001'),
('SEC-LG101-01', 'LG101.01', 'HK1-2025', 35, 33, 'Thu 15:00-17:00', 'LG101', 'GVLG0001');

-- REGISTRATION RECORDS
INSERT INTO RegistrationRecords (registrationID, studentID, status, registrationDate, batchID, sectionID) VALUES
('REG-IT-000001', '202501000001', 'REGISTERED', '2025-01-06', '125IT1', 'SEC-IT101-01'),
('REG-IT-000002', '202501000001', 'REGISTERED', '2025-01-06', '125IT1', 'SEC-IT201-01'),
('REG-LG-000001', '202502000001', 'REGISTERED', '2025-01-07', '125LG1', 'SEC-LG101-01'),
('REG-IT-000003', '202501000002', 'CANCELLED',  '2025-01-08', '125IT2', 'SEC-IT201-01');

-- WAILIST RECORDS
INSERT INTO WaitlistRecords (waitlistID, studentID, sectionID, requestDate, position, status) VALUES
('WAIT-IT-000001', '202501000002', 'SEC-IT201-01', '2025-01-08', 1, 'WAITING'),
('WAIT-LG-000001', '202502000001', 'SEC-LG101-01', '2025-01-09', 1, 'WAITING');