
#"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d am_cdm
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

psql -U postgres -d am_cdm -f reset.sql
psql -U postgres -d am_cdm -f schema.sql


"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d am_cdm

\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/amsystem_02.sql'
\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/material_03.sql'
\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/base_04.sql'
\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/partdesign_05.sql'
\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/parameter_07.sql'
\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/build_08.sql'
\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/builtpart_09.sql'
\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/process_06.sql'
\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/tic_10.sql'
\i 'C:/Users/Kayleigh/DIGITAL_ARCH_REPO/RPMI_DATA_DEV/database/testresult_11.sql'