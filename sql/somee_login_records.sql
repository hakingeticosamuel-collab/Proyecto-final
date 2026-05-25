-- Schema de apoyo para Render/Somee: login, auditoría y registros del proyecto.
-- Ejecuta este script en la base de datos SQL Server de Somee.

IF NOT EXISTS (
    SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[app_users]') AND type IN (N'U')
)
BEGIN
    CREATE TABLE app_users (
        UserId INT IDENTITY(1,1) PRIMARY KEY,
        Username NVARCHAR(128) NOT NULL UNIQUE,
        PasswordHash NVARCHAR(256) NOT NULL,
        DisplayName NVARCHAR(150) NOT NULL,
        Role NVARCHAR(50) NOT NULL DEFAULT 'user',
        CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;

IF NOT EXISTS (
    SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[audit_logs]') AND type IN (N'U')
)
BEGIN
    CREATE TABLE audit_logs (
        AuditId INT IDENTITY(1,1) PRIMARY KEY,
        UserId INT NULL REFERENCES app_users(UserId),
        Username NVARCHAR(128) NULL,
        ActionType NVARCHAR(100) NOT NULL,
        Detail NVARCHAR(512) NULL,
        CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;

IF NOT EXISTS (
    SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[project_records]') AND type IN (N'U')
)
BEGIN
    CREATE TABLE project_records (
        RecordId INT IDENTITY(1,1) PRIMARY KEY,
        DeviceId NVARCHAR(80) NOT NULL,
        MeasurementDate DATETIME2 NOT NULL,
        Value FLOAT NOT NULL,
        Status NVARCHAR(80) NOT NULL DEFAULT 'Activo',
        CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;

IF NOT EXISTS (SELECT 1 FROM app_users WHERE Username = 'admin')
BEGIN
    INSERT INTO app_users (Username, PasswordHash, DisplayName, Role)
    VALUES (
        'admin',
        'scrypt:32768:8:1$iGG4t70nk8MLATBH$6b3f555a358ac0a81a5c2ff8eb676fe06489677cfce5025458722f438f3eaab89e9c56b1988f717211b6ebbe8e2ef8714516d1dcb84ac6f516e964dbeba5f21e',
        'Administrador',
        'admin'
    );
END;

IF NOT EXISTS (SELECT 1 FROM project_records)
BEGIN
    INSERT INTO project_records (DeviceId, MeasurementDate, Value, Status)
    VALUES
        ('Poste-01', SYSUTCDATETIME(), 12.5, 'Activo'),
        ('Poste-02', SYSUTCDATETIME(), 8.1, 'Activo'),
        ('Poste-03', SYSUTCDATETIME(), 0.0, 'Inactivo');
END;
