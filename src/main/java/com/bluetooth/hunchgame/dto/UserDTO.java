package com.bluetooth.hunchgame.dto;

import java.util.List;

public class UserDTO {
    private Long userId;
    private String gender;
    private int age;
    private List<String> preferredPlaces;

    public UserDTO(Long userId, String gender, int age, List<String> preferredPlaces) {
        this.userId = userId;
        this.gender = gender;
        this.age = age;
        this.preferredPlaces = preferredPlaces;
    }

    // Default constructor (if needed)
    public UserDTO() {
    }

    // Getters and setters
    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public List<String> getPreferredPlaces() {
        return preferredPlaces;
    }

    public void setPreferredPlaces(List<String> preferredPlaces) {
        this.preferredPlaces = preferredPlaces;
    }
}

