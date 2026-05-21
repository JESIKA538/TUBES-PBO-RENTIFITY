package com.rentifity.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UpdateProfileRequest {

    private String name;

    private String email;

    private String password;

    private String phone;

    private String occupation;

    private String address;

    private String avatar;
}
