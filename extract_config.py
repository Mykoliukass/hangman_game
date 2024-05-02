from configurations import configurations

print(f"export CONTAINER_NAME={configurations.CONTAINER_NAME}")
print(f"export IMAGE_NAME={configurations.IMAGE_NAME}")
print(f"export HOST={configurations.MONGO_HOST}")
print(f"export PORT={configurations.MONGO_PORT}")
print(f"export DATABASE_NAME={configurations.DATABASE_NAME}")
