def product_directory_path(instance, filename: str) -> str:
    return f"products/{instance.category}/{filename}"
