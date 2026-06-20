package com.rentifity.dto.request;

public class UpdateProfileRequest {

    private String name;

    private String email;

    private String password;

    private String phone;

    private String occupation;

    private String address;

    private String avatar;

    public UpdateProfileRequest() {
    }

    public UpdateProfileRequest(String name, String email, String password, String phone, String occupation, String address, String avatar) {
        this.name = name;
        this.email = email;
        this.password = password;
        this.phone = phone;
        this.occupation = occupation;
        this.address = address;
        this.avatar = avatar;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }

    public String getOccupation() { return occupation; }
    public void setOccupation(String occupation) { this.occupation = occupation; }

    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }

    public String getAvatar() { return avatar; }
    public void setAvatar(String avatar) { this.avatar = avatar; }
}
