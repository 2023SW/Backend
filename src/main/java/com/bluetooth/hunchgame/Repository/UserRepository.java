package com.bluetooth.hunchgame.Repository;

import com.bluetooth.hunchgame.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
public interface UserRepository extends JpaRepository<User, Long>{
    User findByEmail(String email);
}
