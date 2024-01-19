CREATE OR REPLACE TABLE DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE (
	POSTAL_SITE_ID NUMBER(38,0) AUTOINCREMENT COMMENT 'Auto Increment and PK of this table',
	REGION VARCHAR(200) ,
	COUNTRY_NAME VARCHAR(200) ,
	COUNTRY_CODE VARCHAR(2) ,
	COUNTRY_CODE_3_DIGIT VARCHAR(3),
	POSTAL_SYSTEM_NAME VARCHAR(1000),
	POSTAL_SYSTEM_URL VARCHAR(1000),
	POSTAL_SYSTEM_TRACKING_URL VARCHAR(2000),
	LANGUAGE VARCHAR(200),
	CAPTCHA_IND BOOLEAN,
	SELECT_SQL VARCHAR(5000),
    MIN_SELECTED_DAYS NUMBER,
    MAX_SELECTED_DAYS NUMBER,
	IS_ACTIVE BOOLEAN
	);

SELECT * FROM DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE;

TRUNCATE TABLE DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE;

 INSERT INTO DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE (REGION,COUNTRY_NAME,COUNTRY_CODE,COUNTRY_CODE_3_DIGIT,POSTAL_SYSTEM_NAME,POSTAL_SYSTEM_URL,POSTAL_SYSTEM_TRACKING_URL,LANGUAGE,CAPTCHA_IND,SELECT_SQL,MIN_SELECTED_DAYS,MAX_SELECTED_DAYS,IS_ACTIVE)
VALUES('EUROPE','UNITED KINGDOM','GB','GBR','ROYAL MAIL','https://www.royalmail.com/','https://www.royalmail.com/track-your-item','ENGLISH','NO','SELECT TRACKINGNO FROM (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME
FROM (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP)) P
INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE ''%USPS%''
INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))=''#COUNTRY_NAME#''
INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID
GROUP BY P.TRACKINGNO
) WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP);','-7','-30','YES');


INSERT INTO DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE (REGION,COUNTRY_NAME,COUNTRY_CODE,COUNTRY_CODE_3_DIGIT,POSTAL_SYSTEM_NAME,POSTAL_SYSTEM_URL,POSTAL_SYSTEM_TRACKING_URL,LANGUAGE,CAPTCHA_IND,SELECT_SQL,MIN_SELECTED_DAYS,MAX_SELECTED_DAYS,IS_ACTIVE)
VALUES('EUROPE','SPAIN','ES','ESP','CORREOS','https://www.correos.es/','https://www.correos.es/es/en/tools/tracker/items','ENGLISH','NO','SELECT TRACKINGNO FROM (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME
FROM (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP)) P
INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE ''%USPS%''
INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))=''#COUNTRY_NAME#''
INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID
GROUP BY P.TRACKINGNO
) WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP);','-7','-30','YES');

INSERT INTO DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE (REGION,COUNTRY_NAME,COUNTRY_CODE,COUNTRY_CODE_3_DIGIT,POSTAL_SYSTEM_NAME,POSTAL_SYSTEM_URL,POSTAL_SYSTEM_TRACKING_URL,LANGUAGE,CAPTCHA_IND,SELECT_SQL,MIN_SELECTED_DAYS,MAX_SELECTED_DAYS,IS_ACTIVE)
VALUES('SOUTH AMERICA','BRAZIL','BR','BRA','CORREIOS','http://www.correios.com.br/','https://www2.correios.com.br/sistemas/rastreamento/default.cfm','PORTUGUESE','YES','SELECT TRACKINGNO FROM (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME
FROM (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP)) P
INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE ''%USPS%''
INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))=''#COUNTRY_NAME#''
INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID
GROUP BY P.TRACKINGNO
) WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP);','-7','-30','YES');

INSERT INTO DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE (REGION,COUNTRY_NAME,COUNTRY_CODE,COUNTRY_CODE_3_DIGIT,POSTAL_SYSTEM_NAME,POSTAL_SYSTEM_URL,POSTAL_SYSTEM_TRACKING_URL,LANGUAGE,CAPTCHA_IND,SELECT_SQL,MIN_SELECTED_DAYS,MAX_SELECTED_DAYS,IS_ACTIVE)
VALUES('EUROPE','GERMARNY','DE','DEU','DEUTSCHE POST','https://www.deutschepost.de/','https://www.deutschepost.de/sendung/simpleQuery.html','GERMAN','NO','SELECT TRACKINGNO FROM (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME
FROM (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP)) P
INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE ''%USPS%''
INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))=''#COUNTRY_NAME#''
INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID
GROUP BY P.TRACKINGNO
) WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP);','-7','-30','YES');

INSERT INTO DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE (REGION,COUNTRY_NAME,COUNTRY_CODE,COUNTRY_CODE_3_DIGIT,POSTAL_SYSTEM_NAME,POSTAL_SYSTEM_URL,POSTAL_SYSTEM_TRACKING_URL,LANGUAGE,CAPTCHA_IND,SELECT_SQL,MIN_SELECTED_DAYS,MAX_SELECTED_DAYS,IS_ACTIVE)
VALUES('EUROPE','FRANCE','FR','FRA','LA POSTE','https://www.laposte.fr/','https://www.laposte.fr/outils/track-a-parcel','ENGLISH','NO','SELECT TRACKINGNO FROM (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME
FROM (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP)) P
INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE ''%USPS%''
INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))=''#COUNTRY_NAME#''
INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID
GROUP BY P.TRACKINGNO
) WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP);','-7','-30','YES');

INSERT INTO DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE (REGION,COUNTRY_NAME,COUNTRY_CODE,COUNTRY_CODE_3_DIGIT,POSTAL_SYSTEM_NAME,POSTAL_SYSTEM_URL,POSTAL_SYSTEM_TRACKING_URL,LANGUAGE,CAPTCHA_IND,SELECT_SQL,MIN_SELECTED_DAYS,MAX_SELECTED_DAYS,IS_ACTIVE)
VALUES('EAST ASIA','JAPAN','JP','JPN','JAPAN POST','https://www.post.japanpost.jp/','https://www.post.japanpost.jp/index_en.html','ENGLISH','NO','SELECT TRACKINGNO FROM (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME
FROM (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP)) P
INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE ''%USPS%''
INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))=''#COUNTRY_NAME#''
INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID
GROUP BY P.TRACKINGNO
) WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP);','-7','-30','YES');

INSERT INTO DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE (REGION,COUNTRY_NAME,COUNTRY_CODE,COUNTRY_CODE_3_DIGIT,POSTAL_SYSTEM_NAME,POSTAL_SYSTEM_URL,POSTAL_SYSTEM_TRACKING_URL,LANGUAGE,CAPTCHA_IND,SELECT_SQL,MIN_SELECTED_DAYS,MAX_SELECTED_DAYS,IS_ACTIVE)
VALUES('EUROPE','AUSTRIA','AT','AUT','AUSTRIAN POST','https://www.post.at/','https://www.post.at/s/sendungssuche','ENGLISH','NO','SELECT TRACKINGNO FROM (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME
FROM (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP)) P
INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE ''%USPS%''
INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))=''#COUNTRY_NAME#''
INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID
GROUP BY P.TRACKINGNO
) WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP);','-7','-30','YES');

INSERT INTO DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE (REGION,COUNTRY_NAME,COUNTRY_CODE,COUNTRY_CODE_3_DIGIT,POSTAL_SYSTEM_NAME,POSTAL_SYSTEM_URL,POSTAL_SYSTEM_TRACKING_URL,LANGUAGE,CAPTCHA_IND,SELECT_SQL,MIN_SELECTED_DAYS,MAX_SELECTED_DAYS,IS_ACTIVE)
VALUES('EUROPE','ITALY','IT','ITA','POSTE ITALIANE','https://www.poste.it/','https://www.poste.it/','ITALIAN','NO','SELECT TRACKINGNO FROM (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME
FROM (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP)) P
INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE ''%USPS%''
INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))=''#COUNTRY_NAME#''
INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID
GROUP BY P.TRACKINGNO
) WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,#MAX_SELECTED_DAYS#,CURRENT_TIMESTAMP) AND DATEADD(DAY,#MIN_SELECTED_DAYS#,CURRENT_TIMESTAMP);','-7','-30','YES');
