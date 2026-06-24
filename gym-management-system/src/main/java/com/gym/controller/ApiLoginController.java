package com.gym.controller;

import com.gym.pojo.Admin;
import com.gym.pojo.Member;
import com.gym.service.AdminService;
import com.gym.service.EmployeeService;
import com.gym.service.EquipmentService;
import com.gym.service.MemberService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import jakarta.servlet.http.HttpSession;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.regex.Pattern;

@RestController
@RequestMapping("/api")
public class ApiLoginController {

    private static final String SESSION_ADMIN = "admin";
    private static final String SESSION_USER = "user";

    private final MemberService memberService;
    private final AdminService adminService;
    private final EmployeeService employeeService;
    private final EquipmentService equipmentService;

    public ApiLoginController(
            MemberService memberService,
            AdminService adminService,
            EmployeeService employeeService,
            EquipmentService equipmentService) {
        this.memberService = memberService;
        this.adminService = adminService;
        this.employeeService = employeeService;
        this.equipmentService = equipmentService;
    }

    @PostMapping("/adminLogin")
    public ResponseEntity<Map<String, Object>> adminLogin(Admin admin, HttpSession session) {
        Admin loggedIn = adminService.adminLogin(admin);
        if (loggedIn == null) {
            return unauthorized("账号或密码有误");
        }
        putAdminMainDataInSession(session, loggedIn);
        return ResponseEntity.ok(singleSuccess());
    }

    @PostMapping("/userLogin")
    public ResponseEntity<Map<String, Object>> userLogin(
            @RequestParam(required = false) String username,
            @RequestParam(required = false) String password,
            HttpSession session) {
        
        if (username == null || username.isBlank()) {
            return badRequest("请输入用户名");
        }
        if (password == null || password.isBlank()) {
            return badRequest("请输入密码");
        }
        
        Member loggedIn = null;
        List<Member> members = memberService.findAll();
        for (Member m : members) {
            if (m.getMemberName() != null && m.getMemberName().equals(username) && 
                m.getMemberPassword() != null && m.getMemberPassword().equals(password)) {
                loggedIn = m;
                break;
            }
        }
        
        if (loggedIn == null) {
            return unauthorized("用户名或密码有误");
        }
        session.setAttribute(SESSION_USER, loggedIn);
        return ResponseEntity.ok(singleSuccess());
    }

    @PostMapping("/logout")
    public ResponseEntity<Map<String, Object>> logout(HttpSession session) {
        session.invalidate();
        return ResponseEntity.ok(singleSuccess());
    }

    @PostMapping("/userRegister")
    public ResponseEntity<Map<String, Object>> userRegister(
            @RequestParam(required = false) String memberUsername,
            @RequestParam(required = false) String memberEmail,
            @RequestParam(required = false) String memberPassword) {
        String username = memberUsername;
        String email = memberEmail;
        String password = memberPassword;

        if (username == null || username.isBlank()) {
            return badRequest("用户名不能为空");
        }
        if (!Pattern.matches("^[\\u4e00-\\u9fa5a-zA-Z0-9_]{6,20}$", username)) {
            return badRequest("用户名须为6-20位中文、英文、数字或下划线");
        }
        
        List<Member> existingMembers = memberService.selectByMemberAccount(0);
        for (Member m : existingMembers) {
            if (m.getMemberName() != null && m.getMemberName().equals(username)) {
                return conflict("用户名已存在");
            }
        }
        
        if (email == null || email.isBlank()) {
            return badRequest("邮箱不能为空");
        }
        if (!Pattern.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$", email)) {
            return badRequest("邮箱格式不正确");
        }
        if (password == null || password.isBlank()) {
            return badRequest("密码不能为空");
        }
        if (!Pattern.matches("^(?=.*[A-Za-z])(?=.*\\d)(?=.*[@$!%*?&_#^~.,:;\\-+=|\\/\\[\\]{}()<>])[A-Za-z\\d@$!%*?&_#^~.,:;\\-+=|\\/\\[\\]{}()<>]{8,}$", password)) {
            return badRequest("密码至少8位，且需包含字母、数字及特殊符号");
        }

        Integer account = generateUniqueAccount();
        Date date = new Date();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        String nowDay = sdf.format(date);

        Member member = new Member();
        member.setMemberAccount(account);
        member.setMemberName(username);
        member.setMemberPassword(password);
        member.setCardTime(nowDay);
        member.setCardClass(0);
        member.setCardNextClass(0);

        Boolean ok = memberService.registerMember(member);
        if (ok == null || !ok) {
            return internalError("注册失败，请稍后重试");
        }

        Map<String, Object> resp = new HashMap<>();
        resp.put("success", true);
        resp.put("username", username);
        return ResponseEntity.ok(resp);
    }

    @GetMapping("/toAdminMain")
    public ResponseEntity<Map<String, Object>> toAdminMain(HttpSession session) {
        Map<String, Object> body = new HashMap<>();
        body.put("success", true);
        body.put("memberTotal", session.getAttribute("memberTotal"));
        body.put("employeeTotal", session.getAttribute("employeeTotal"));
        body.put("humanTotal", session.getAttribute("humanTotal"));
        body.put("equipmentTotal", session.getAttribute("equipmentTotal"));
        return ResponseEntity.ok(body);
    }

    @GetMapping("/toUserMain")
    public ResponseEntity<Map<String, Object>> toUserMain(HttpSession session) {
        Map<String, Object> body = new HashMap<>();
        body.put("success", true);
        body.put("member", session.getAttribute(SESSION_USER));
        return ResponseEntity.ok(body);
    }

    /** 管理员登录后写入 session：身份 + 主页统计（与原先 adminMain 依赖的 key 一致）。 */
    private void putAdminMainDataInSession(HttpSession session, Admin admin) {
        session.setAttribute(SESSION_ADMIN, admin);
        Integer memberTotal = memberService.selectTotalCount();
        Integer employeeTotal = employeeService.selectTotalCount();
        Integer humanTotal = memberTotal + employeeTotal;
        Integer equipmentTotal = equipmentService.selectTotalCount();
        session.setAttribute("memberTotal", memberTotal);
        session.setAttribute("employeeTotal", employeeTotal);
        session.setAttribute("humanTotal", humanTotal);
        session.setAttribute("equipmentTotal", equipmentTotal);
    }

    private static Map<String, Object> singleSuccess() {
        Map<String, Object> m = new HashMap<>(2);
        m.put("success", true);
        return m;
    }

    private static ResponseEntity<Map<String, Object>> unauthorized(String message) {
        Map<String, Object> m = new HashMap<>(4);
        m.put("success", false);
        m.put("message", message);
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(m);
    }

    private static ResponseEntity<Map<String, Object>> badRequest(String message) {
        Map<String, Object> m = new HashMap<>(4);
        m.put("success", false);
        m.put("message", message);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(m);
    }

    private static ResponseEntity<Map<String, Object>> conflict(String message) {
        Map<String, Object> m = new HashMap<>(4);
        m.put("success", false);
        m.put("message", message);
        return ResponseEntity.status(HttpStatus.CONFLICT).body(m);
    }

    private static ResponseEntity<Map<String, Object>> internalError(String message) {
        Map<String, Object> m = new HashMap<>(4);
        m.put("success", false);
        m.put("message", message);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(m);
    }

    private Integer generateUniqueAccount() {
        Random random = new Random();
        for (int attempt = 0; attempt < 10; attempt++) {
            String account = "2021";
            for (int i = 0; i < 5; i++) {
                account += random.nextInt(10);
            }
            Integer result = Integer.parseInt(account);
            List<Member> existing = memberService.selectByMemberAccount(result);
            if (existing == null || existing.isEmpty()) {
                return result;
            }
        }
        throw new IllegalStateException("无法生成唯一会员账号");
    }
}