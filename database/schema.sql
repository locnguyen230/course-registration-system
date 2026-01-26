-- Bảng người dùng
CREATE TABLE User (
    userID CHAR(36) PRIMARY KEY,
    userName VARCHAR(16),
    password VARCHAR(255),
    role VARCHAR(11),
    status VARCHAR(8)
);

-- Bảng sinh viên
CREATE TABLE Student (
    studentID CHAR(12) PRIMARY KEY,
    fullName VARCHAR(50),
    email VARCHAR(255),
    major VARCHAR(255),
    yearLevel INT,
    academicStatus VARCHAR(9),
    userID CHAR(36),
    FOREIGN KEY (userID) REFERENCES User(userID)
);

-- Bảng giảng viên
CREATE TABLE Instructor (
    instructorID CHAR(10) PRIMARY KEY,
    fullName VARCHAR(50),
    department VARCHAR(20),
    userID CHAR(36),
    FOREIGN KEY (userID) REFERENCES User(userID)
);

-- Bảng quản trị viên
CREATE TABLE Administration (
    adminID CHAR(10) PRIMARY KEY,
    fullName VARCHAR(18),
    userID CHAR(36),
    FOREIGN KEY (userID) REFERENCES User(userID)
);

-- Cấu hình học vụ
CREATE TABLE AcademicConfiguration (
    configID CHAR(20) PRIMARY KEY,
    academicYear VARCHAR(9),
    semester VARCHAR(9),
    policies TEXT,
    adminID CHAR(10),
    FOREIGN KEY (adminID) REFERENCES Administration(adminID)
);

-- Đợt đăng ký
CREATE TABLE RegistrationBatch (
    batchID CHAR(6) PRIMARY KEY,
    semester VARCHAR(9),
    startTime DATETIME,
    endTime DATETIME,
    eligibleYearLevel INT,
    adminID CHAR(10),
    FOREIGN KEY (adminID) REFERENCES Administration(adminID)
);

-- Bảng khóa học
CREATE TABLE Course (
    courseID CHAR(8) PRIMARY KEY,
    courseName VARCHAR(255),
    credits INT,
    description TEXT
);

-- Bảng học phần
CREATE TABLE CourseSection (
    sectionID CHAR(12) PRIMARY KEY,
    sectionCode VARCHAR(255),
    semester VARCHAR(9),
    capacity INT,
    enrolledCount INT,
    schedule VARCHAR(255),
    courseID CHAR(8),
    instructorID CHAR(10),
    FOREIGN KEY (courseID) REFERENCES Course(courseID),
    FOREIGN KEY (instructorID) REFERENCES Instructor(instructorID)
);

-- Bảng đăng ký học
CREATE TABLE RegistrationRecords (
    registrationID CHAR(15) PRIMARY KEY,
    studentID CHAR(12),
    status VARCHAR(10),
    registrationDate DATE,
    batchID CHAR(6),
    sectionID CHAR(12),
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (batchID) REFERENCES RegistrationBatch(batchID),
    FOREIGN KEY (sectionID) REFERENCES CourseSection(sectionID)
);

-- Bảng danh sách chờ
CREATE TABLE WaitlistRecords (
    waitlistID CHAR(15) PRIMARY KEY,
    studentID CHAR(12),
    sectionID CHAR(12),
    requestDate DATE,
    position INT,
    status VARCHAR(8),
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (sectionID) REFERENCES CourseSection(sectionID)
);

-- Bảng điều kiện tiên quyết
CREATE TABLE CoursePrerequisites (
    prerequisiteID CHAR(8),
    courseID CHAR(8),
    PRIMARY KEY (prerequisiteID, courseID),
    FOREIGN KEY (prerequisiteID) REFERENCES Course(courseID),
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);


-- User role in the system:
-- ADMIN      : System administrator
-- STUDENT    : Student user
-- INSTRUCTOR : Instructor user
ALTER TABLE User
ADD CONSTRAINT chk_user_role
CHECK (role IN ('ADMIN', 'STUDENT', 'INSTRUCTOR'));


-- User account status:
-- ACTIVE   : Account is active
-- INACTIVE : Account is temporarily disabled
-- LOCKED   : Account is locked by administrator
ALTER TABLE User
ADD CONSTRAINT chk_user_status
CHECK (status IN ('ACTIVE', 'INACTIVE', 'LOCKED'));


-- Academic status of a student:
-- ENROLLED  : Currently studying
-- SUSPENDED : Temporarily suspended
-- GRADUATED : Completed the program
ALTER TABLE Student
ADD CONSTRAINT chk_student_academic_status
CHECK (academicStatus IN ('ENROLLED', 'SUSPENDED', 'GRADUATED'));

-- Registration status:
-- REGISTERED : Student successfully registered
-- CANCELLED  : Registration cancelled
-- COMPLETED  : Course completed
ALTER TABLE RegistrationRecords
ADD CONSTRAINT chk_registration_status
CHECK (status IN ('REGISTERED', 'CANCELLED', 'COMPLETED'));


-- Waitlist status:
-- WAITING  : Student is waiting for an available slot
-- APPROVED : Student approved from the waitlist
-- REMOVED  : Student removed from the waitlist
ALTER TABLE WaitlistRecords
ADD CONSTRAINT chk_waitlist_status
CHECK (status IN ('WAITING', 'APPROVED', 'REMOVED'));


-- Section capacity must be zero or greater
ALTER TABLE CourseSection
ADD CONSTRAINT chk_capacity_positive
CHECK (capacity >= 0),

-- Enrolled student count must be zero or greater
ADD CONSTRAINT chk_enrolledCount_nonnegative
CHECK (enrolledCount >= 0),

-- Enrolled students must not exceed section capacity
ADD CONSTRAINT chk_enrolled_not_exceed_capacity
CHECK (enrolledCount <= capacity);
