package com.bluetooth.hunchgame.controller;

import com.bluetooth.hunchgame.dto.UserDTO;
import com.bluetooth.hunchgame.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private LoginService loginService;

    @PostMapping("api/userInfo")
    public ResponseEntity<String> createUser(@RequestBody UserDTO userDto) {
        // Map the UserDTO to your User entity and save it using the UserService
        // Example: userService.createUser(userMapper.toEntity(userDto));
        return ResponseEntity.ok("User created successfully");
    }
}
