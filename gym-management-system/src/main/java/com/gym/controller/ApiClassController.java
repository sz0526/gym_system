package com.gym.controller;

import com.gym.pojo.ClassOrder;
import com.gym.pojo.ClassTable;
import com.gym.service.ClassOrderService;
import com.gym.service.ClassTableService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/class")
public class ApiClassController {

    @Autowired
    private ClassTableService classTableService;
    @Autowired
    private ClassOrderService classOrderService;

    @GetMapping("/selClass")
    public Map<String, Object> selectClass() {
        List<ClassTable> classList = classTableService.findAll();
        Map<String, Object> resp = new HashMap<>();
        resp.put("success", true);
        resp.put("classList", classList);
        return resp;
    }

    @GetMapping("/selClassOrder")
    public Map<String, Object> selectClassOrder(Integer classId) {
        List<ClassOrder> classOrderList = classOrderService.selectMemberOrderList(classId);
        Map<String, Object> resp = new HashMap<>();
        resp.put("success", true);
        resp.put("classOrderList", classOrderList);
        return resp;
    }

    @GetMapping("/toAddClass")
    public Map<String, Object> toAddClass() {
        Map<String, Object> resp = new HashMap<>();
        resp.put("success", true);
        return resp;
    }

    // 按会员账号查询已报名课程（给 AI 工具调用）
    @GetMapping("/getClassByMember")
    public Map<String, Object> getClassByMember(@RequestParam String memberAccount) {
        Map<String, Object> resp = new HashMap<>();
        try {
            List<ClassOrder> orders = classOrderService.selectClassOrderByMemberAccount(
                    Integer.parseInt(memberAccount)
            );
            resp.put("success", true);
            resp.put("orders", orders);
        } catch (Exception e) {
            resp.put("success", false);
            resp.put("message", e.getMessage());
        }
        return resp;
    }

    // 查询所有课程表（给 AI 工具调用）
    @GetMapping("/getAllClass")
    public Map<String, Object> getAllClass() {
        Map<String, Object> resp = new HashMap<>();
        try {
            List<ClassTable> classList = classTableService.findAll();
            resp.put("success", true);
            resp.put("classList", classList);
        } catch (Exception e) {
            resp.put("success", false);
            resp.put("message", e.getMessage());
        }
        return resp;
    }

    @PostMapping("/addClass")
    public ResponseEntity<Map<String, Object>> addClass(ClassTable classTable) {
        classTableService.insertClass(classTable);
        Map<String, Object> resp = new HashMap<>();
        resp.put("success", true);
        return ResponseEntity.ok(resp);
    }

    @PostMapping("/delClass")
    public ResponseEntity<Map<String, Object>> deleteClass(Integer classId) {
        classTableService.deleteClassByClassId(classId);
        classTableService.deleteOrderByClassId(classId);
        Map<String, Object> resp = new HashMap<>();
        resp.put("success", true);
        return ResponseEntity.ok(resp);
    }
}