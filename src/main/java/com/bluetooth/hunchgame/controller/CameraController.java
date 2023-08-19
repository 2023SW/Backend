package com.bluetooth.hunchgame.controller;

import com.bluetooth.hunchgame.Request.CameraRequest;
import com.bluetooth.hunchgame.service.CameraService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CameraController {
    private final CameraService cameraService;


    @Autowired
    public CameraController(CameraService cameraService){
        this.cameraService = cameraService;
    }

    @PostMapping("/api/cameraService")
    public ResponseEntity<String> calculateCongestion(@RequestBody CameraRequest request){
        int count = request.getCount();
        String congestion = cameraService.calculateCongestion(count);
        return ResponseEntity.ok(congestion);
    }
}
