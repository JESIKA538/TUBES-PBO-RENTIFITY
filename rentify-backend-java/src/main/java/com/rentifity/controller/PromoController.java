package com.rentifity.controller;
import com.rentifity.model.Promo;
import com.rentifity.repository.PromoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/promos")
public class PromoController {
    @Autowired
    private PromoRepository promoRepository;
    
    @GetMapping("/validate")
    public ResponseEntity<?> validatePromo(@RequestParam String code) {
        Optional<Promo> promo = promoRepository.findByCodeAndIsActiveTrue(code);
        if (promo.isPresent()) {
            return ResponseEntity.ok(promo.get());
        }
        return ResponseEntity.badRequest().body(Map.of("message", "Kode promo tidak valid atau sudah kadaluarsa"));
    }
}
