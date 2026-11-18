package com.devops.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class JenkinsTroubleshooterApplication {

    public static void main(String[] args) {
        SpringApplication.run(JenkinsTroubleshooterApplication.class, args);
    }

    @GetMapping("/health")
    public String health() {
        return "Jenkins AI Troubleshooter is running!";
    }
}
