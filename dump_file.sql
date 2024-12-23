USE [master]
GO
/****** Object:  Database [学生成绩管理]    Script Date: 2024/11/17 20:34:57 ******/
CREATE DATABASE [学生成绩管理]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'学生成绩管理', FILENAME = N'D:\SQL Server\MSSQL15.NEWEST\MSSQL\DATA\学生成绩管理.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'学生成绩管理_log', FILENAME = N'D:\SQL Server\MSSQL15.NEWEST\MSSQL\DATA\学生成绩管理_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [学生成绩管理] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [学生成绩管理].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [学生成绩管理] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [学生成绩管理] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [学生成绩管理] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [学生成绩管理] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [学生成绩管理] SET ARITHABORT OFF 
GO
ALTER DATABASE [学生成绩管理] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [学生成绩管理] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [学生成绩管理] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [学生成绩管理] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [学生成绩管理] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [学生成绩管理] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [学生成绩管理] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [学生成绩管理] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [学生成绩管理] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [学生成绩管理] SET  DISABLE_BROKER 
GO
ALTER DATABASE [学生成绩管理] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [学生成绩管理] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [学生成绩管理] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [学生成绩管理] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [学生成绩管理] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [学生成绩管理] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [学生成绩管理] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [学生成绩管理] SET RECOVERY FULL 
GO
ALTER DATABASE [学生成绩管理] SET  MULTI_USER 
GO
ALTER DATABASE [学生成绩管理] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [学生成绩管理] SET DB_CHAINING OFF 
GO
ALTER DATABASE [学生成绩管理] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [学生成绩管理] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [学生成绩管理] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [学生成绩管理] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'学生成绩管理', N'ON'
GO
ALTER DATABASE [学生成绩管理] SET QUERY_STORE = OFF
GO
USE [学生成绩管理]
GO
/****** Object:  User [teacher_username]    Script Date: 2024/11/17 20:34:57 ******/
CREATE USER [teacher_username] FOR LOGIN [teacher_login] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [student_username]    Script Date: 2024/11/17 20:34:57 ******/
CREATE USER [student_username] FOR LOGIN [student_login] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [admin_username]    Script Date: 2024/11/17 20:34:57 ******/
CREATE USER [admin_username] FOR LOGIN [admin_login] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  DatabaseRole [TeacherRole]    Script Date: 2024/11/17 20:34:57 ******/
CREATE ROLE [TeacherRole]
GO
/****** Object:  DatabaseRole [StudentRole]    Script Date: 2024/11/17 20:34:57 ******/
CREATE ROLE [StudentRole]
GO
/****** Object:  DatabaseRole [AdminRole]    Script Date: 2024/11/17 20:34:57 ******/
CREATE ROLE [AdminRole]
GO
ALTER ROLE [TeacherRole] ADD MEMBER [teacher_username]
GO
ALTER ROLE [StudentRole] ADD MEMBER [student_username]
GO
ALTER ROLE [AdminRole] ADD MEMBER [admin_username]
GO
/****** Object:  Table [dbo].[Admins]    Script Date: 2024/11/17 20:34:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Admins](
	[AdminID] [int] NULL,
	[AdminName] [nvarchar](50) NULL,
	[username] [varchar](50) NULL,
	[password] [varchar](50) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Classes]    Script Date: 2024/11/17 20:34:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Classes](
	[ClassID] [int] NOT NULL,
	[CourseID] [int] NOT NULL,
	[TeacherID] [int] NOT NULL,
 CONSTRAINT [PK_Classes] PRIMARY KEY CLUSTERED 
(
	[ClassID] ASC,
	[CourseID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Courses]    Script Date: 2024/11/17 20:34:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Courses](
	[CourseID] [int] NOT NULL,
	[CourseName] [nvarchar](10) NULL,
	[Credit] [int] NULL,
 CONSTRAINT [PK_Courses] PRIMARY KEY CLUSTERED 
(
	[CourseID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Grades]    Script Date: 2024/11/17 20:34:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Grades](
	[StudentID] [int] NOT NULL,
	[CourseID] [int] NOT NULL,
	[Score] [int] NULL,
 CONSTRAINT [PK_Grades] PRIMARY KEY CLUSTERED 
(
	[StudentID] ASC,
	[CourseID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Students]    Script Date: 2024/11/17 20:34:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Students](
	[StudentID] [int] NOT NULL,
	[StudentName] [nvarchar](10) NULL,
	[ClassID] [int] NULL,
	[username] [varchar](50) NULL,
	[password] [varchar](50) NULL,
 CONSTRAINT [PK_Students] PRIMARY KEY CLUSTERED 
(
	[StudentID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Teachers]    Script Date: 2024/11/17 20:34:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Teachers](
	[TeacherID] [int] NOT NULL,
	[TeacherName] [nvarchar](10) NULL,
	[Title] [nvarchar](10) NULL,
	[username] [varchar](50) NULL,
	[password] [varchar](50) NULL,
 CONSTRAINT [PK_Teachers] PRIMARY KEY CLUSTERED 
(
	[TeacherID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Index [IX_Classes]    Script Date: 2024/11/17 20:34:57 ******/
CREATE NONCLUSTERED INDEX [IX_Classes] ON [dbo].[Classes]
(
	[ClassID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Classes]  WITH CHECK ADD  CONSTRAINT [FK_Classes_Courses] FOREIGN KEY([ClassID])
REFERENCES [dbo].[Courses] ([CourseID])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Classes] CHECK CONSTRAINT [FK_Classes_Courses]
GO
ALTER TABLE [dbo].[Grades]  WITH CHECK ADD  CONSTRAINT [FK_Grades_Courses] FOREIGN KEY([CourseID])
REFERENCES [dbo].[Courses] ([CourseID])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Grades] CHECK CONSTRAINT [FK_Grades_Courses]
GO
ALTER TABLE [dbo].[Grades]  WITH CHECK ADD  CONSTRAINT [FK_Grades_Students] FOREIGN KEY([StudentID])
REFERENCES [dbo].[Students] ([StudentID])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Grades] CHECK CONSTRAINT [FK_Grades_Students]
GO
ALTER TABLE [dbo].[Classes]  WITH CHECK ADD  CONSTRAINT [chk_class_ClassID] CHECK  (([ClassID]>=(1) AND [ClassID]<=(9)))
GO
ALTER TABLE [dbo].[Classes] CHECK CONSTRAINT [chk_class_ClassID]
GO
ALTER TABLE [dbo].[Students]  WITH CHECK ADD  CONSTRAINT [chk_ClassID] CHECK  (([ClassID]>=(1) AND [ClassID]<=(9)))
GO
ALTER TABLE [dbo].[Students] CHECK CONSTRAINT [chk_ClassID]
GO
/****** Object:  StoredProcedure [dbo].[GetStudentGrades]    Script Date: 2024/11/17 20:34:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[GetStudentGrades]
@studentId INT
AS
BEGIN
    SELECT c.CourseName, g.Score
    FROM Grades g
    JOIN Courses c ON g.CourseID = c.CourseID
    WHERE g.StudentID = @studentId;
END;
GO
USE [master]
GO
ALTER DATABASE [学生成绩管理] SET  READ_WRITE 
GO
