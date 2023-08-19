package com.bluetooth.hunchgame.service;

import org.springframework.stereotype.Service;

@Service
public class CameraService {
    public String calculateCongestion(int count){
        if(count >= 10){
            return "매우 혼잡";
        } else if (count >= 7){
            return"혼잡";
        } else if (count >= 4){
            return"한산";
        } else if (count >= 1){
            return "매우 한산";
        }else {
            return"사람 없음";
        }
    }
}
