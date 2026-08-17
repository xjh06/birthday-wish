package com.example.birthday.common;

import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ApiResponse<Void>> handleBusiness(BusinessException exception) {
        return ResponseEntity
            .status(exception.getStatus())
            .body(ApiResponse.error(exception.getCode(), exception.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Void>> handleValidation(MethodArgumentNotValidException exception) {
        String message = exception.getBindingResult()
            .getFieldErrors()
            .stream()
            .findFirst()
            .map(FieldError::getDefaultMessage)
            .orElse("参数校验失败");
        return ResponseEntity.badRequest().body(ApiResponse.error(400, message));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<Void>> handleUnknown(Exception exception) {
        return ResponseEntity.internalServerError().body(ApiResponse.error(500, "服务器暂时开小差了"));
    }
}
