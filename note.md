1. AWS RDS 創建雲資料庫(選擇Postgressql)
   
   Postgressql連接AWS如遇到連線超時(使用AWS RDS)
   
   - Go to "Security group rules" (under "Connectivity & security")
   - Click the item "default" Security group
   - Click "Actions" > "Edit inbound rules" > "Add rule"
   - Select... Type: "All traffic", Source: "My IP", then click "Save rules"
   
   翻譯
   
   - 點選安全組規則(再連接和安全性下面)
   - 點選 "default" 選項
   - 點選 "操作" > 點選 "編輯入站規則" > 點選 "添加規則"
   - Select... 類型: "所有流量", 源: "我的IP", 點選 "保存規則"


2. AWS S3 跨源资源共享(CORS)

   [
   {
   "AllowedHeaders": [
   "*"
   ],
   "AllowedMethods": [
   "POST",
   "GET",
   "PUT"
   ],
   "AllowedOrigins": [
   "*"
   ]
   }
   ]


3. AWS IAM

   創建用戶 -> 勾選編成訪問 -> 點選 "直接附加現有策略" 搜尋:S3 -> 勾選 "AmazonS3FullAccess"(這將暫時授予用戶所有權限) -> 下一步，下一步，創建 ->
    
   複製訪問密鑰ID

   返回django project setting.py

   AWS_ACCESS_KEY_ID = '*****************'

   AWS_SECRET_ACCESS_KEY = '*****************'

   AWS_STORAGE_BUCKET_NAME = '*****************'

   AWS_S3_FILE_OVERWRITE = False

   AWS_DEFAULT_ACL = None

   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

   STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
