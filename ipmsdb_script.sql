USE [master]
GO
/****** Object:  Database [ipmsDB]    Script Date: 15/04/2024 14:28:32 ******/
CREATE DATABASE [ipmsDB]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'ipmsDB', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL13.SQLEXPRESS\MSSQL\DATA\ipmsDB.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'ipmsDB_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL13.SQLEXPRESS\MSSQL\DATA\ipmsDB_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
GO
ALTER DATABASE [ipmsDB] SET COMPATIBILITY_LEVEL = 130
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [ipmsDB].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [ipmsDB] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [ipmsDB] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [ipmsDB] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [ipmsDB] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [ipmsDB] SET ARITHABORT OFF 
GO
ALTER DATABASE [ipmsDB] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [ipmsDB] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [ipmsDB] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [ipmsDB] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [ipmsDB] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [ipmsDB] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [ipmsDB] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [ipmsDB] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [ipmsDB] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [ipmsDB] SET  DISABLE_BROKER 
GO
ALTER DATABASE [ipmsDB] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [ipmsDB] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [ipmsDB] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [ipmsDB] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [ipmsDB] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [ipmsDB] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [ipmsDB] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [ipmsDB] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [ipmsDB] SET  MULTI_USER 
GO
ALTER DATABASE [ipmsDB] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [ipmsDB] SET DB_CHAINING OFF 
GO
ALTER DATABASE [ipmsDB] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [ipmsDB] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [ipmsDB] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [ipmsDB] SET QUERY_STORE = OFF
GO
USE [ipmsDB]
GO
ALTER DATABASE SCOPED CONFIGURATION SET LEGACY_CARDINALITY_ESTIMATION = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 0;
GO
ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SNIFFING = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET QUERY_OPTIMIZER_HOTFIXES = OFF;
GO
USE [ipmsDB]
GO
/****** Object:  Table [dbo].[Claims]    Script Date: 15/04/2024 14:28:32 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Claims](
	[ClaimID] [varchar](50) NOT NULL,
	[PolicyID] [varchar](50) NULL,
	[CustomerID] [varchar](50) NULL,
	[DateFiled] [date] NOT NULL,
	[Description] [varchar](255) NOT NULL,
	[Amount] [decimal](18, 2) NOT NULL,
	[Status] [varchar](20) NULL,
PRIMARY KEY CLUSTERED 
(
	[ClaimID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Customer]    Script Date: 15/04/2024 14:28:32 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Customer](
	[CustomerID] [varchar](50) NOT NULL,
	[FirstName] [varchar](50) NOT NULL,
	[LastName] [varchar](50) NOT NULL,
	[Username] [varchar](50) NOT NULL,
	[PhoneNumber] [varchar](50) NOT NULL,
	[Email] [varchar](50) NOT NULL,
	[Password] [varchar](250) NOT NULL,
	[role] [varchar](20) NULL,
PRIMARY KEY CLUSTERED 
(
	[CustomerID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[Username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Policies]    Script Date: 15/04/2024 14:28:32 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Policies](
	[PolicyID] [varchar](50) NOT NULL,
	[CustomerID] [varchar](50) NULL,
	[PolicyTypeID] [varchar](50) NULL,
	[ItemInsured] [varchar](255) NOT NULL,
	[InsuredValue] [decimal](18, 2) NOT NULL,
	[MonthlyPremium] [decimal](18, 2) NOT NULL,
	[DateTakenOut] [date] NOT NULL,
	[DateActive] [date] NOT NULL,
	[Status] [varchar](20) NULL,
PRIMARY KEY CLUSTERED 
(
	[PolicyID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PolicyType]    Script Date: 15/04/2024 14:28:32 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PolicyType](
	[PolicyTypeID] [varchar](50) NOT NULL,
	[name] [varchar](50) NOT NULL,
	[description] [varchar](1000) NOT NULL,
	[short_description] [varchar](100) NOT NULL,
	[img] [varchar](255) NOT NULL,
	[alt] [varchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[PolicyTypeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Claims]  WITH CHECK ADD FOREIGN KEY([CustomerID])
REFERENCES [dbo].[Customer] ([CustomerID])
GO
ALTER TABLE [dbo].[Claims]  WITH CHECK ADD FOREIGN KEY([PolicyID])
REFERENCES [dbo].[Policies] ([PolicyID])
GO
ALTER TABLE [dbo].[Policies]  WITH CHECK ADD FOREIGN KEY([CustomerID])
REFERENCES [dbo].[Customer] ([CustomerID])
GO
ALTER TABLE [dbo].[Policies]  WITH CHECK ADD FOREIGN KEY([PolicyTypeID])
REFERENCES [dbo].[PolicyType] ([PolicyTypeID])
GO
USE [master]
GO
ALTER DATABASE [ipmsDB] SET  READ_WRITE 
GO

INSERT INTO policytype
VALUES ('1', 'Car Insurance', 'Description of Car Insurance to be added next', 'Short Description of Car Insurance', 'https://previews.123rf.com/images/enginakyurt/enginakyurt1810/enginakyurt181000239/110640624-toy-cars-close-up-background.jpg', 'placeholder image');

INSERT INTO policytype 
VALUES ('2', 'Legal Insurance', 'Protect yourself and your business with our comprehensive legal insurance offering. Our policy provides coverage for a wide range of legal expenses, including litigation costs, contract disputes, and legal consultations. With our tailored plans, you can safeguard your assets and mitigate financial risks associated with legal challenges. Gain peace of mind knowing that you have expert legal support at your fingertips, allowing you to focus on what matters most – your business's success. Don\'t wai', 'Protect yourself and your business with our comprehensive legal insurance offering.', 'static\images\gavel.jpg', 'placeholder image');

INSERT INTO policytype
VALUES ('3', 'Niche Insurance', 'Description of Niche Insurance', 'Short Description of Niche Insurance', 'https://previews.123rf.com/images/enginakyurt/enginakyurt1810/enginakyurt181000239/110640624-toy-cars-close-up-background.jpg', 'placeholder image');
