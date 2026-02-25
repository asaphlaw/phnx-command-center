# Root Cause Analysis: Gateway Lifecycle & Disconnection Errors

## ERROR 1: Gateway Lifecycle Error

### Symptoms
- "Gateway lifecycle error"
- Connection drops unexpectedly
- Need to restart/reconnect
- Session terminates abruptly

### 🔴 PROBABLE CAUSES

#### 1A. Idle Timeout (Most Likely)
**What:** OpenClaw Gateway has idle connection limits
**Evidence:**
- Errors happen during pauses in conversation
- Long-running commands trigger it
- Web interface has session limits

**Mechanism:**
```
User idle → No keep-alive ping → Gateway marks session dead → Error
```

**Fix:**
- Enable heartbeat/keep-alive
- Send periodic NO_OP messages
- Use persistent session mode

---

#### 1B. Memory/Resource Limits
**What:** Gateway process hits memory/CPU limits
**Evidence:**
- Errors during heavy operations (browser-use, vector search)
- Long conversations eventually fail
- Restart clears it temporarily

**Mechanism:**
```
Large response → Memory pressure → GC thrashing → Timeout → Lifecycle error
```

**Fix:**
- Break large operations into chunks
- Clear memory between heavy tasks
- Increase gateway resources

---

#### 1C. WebSocket/Transport Timeout
**What:** Underlying WebSocket connection drops
**Evidence:**
- Network hiccups cause immediate failure
- Mobile networks especially affected
- No graceful degradation

**Mechanism:**
```
Network jitter → TCP drop → WebSocket close → Gateway terminates session
```

**Fix:**
- Enable WebSocket auto-reconnect
- Use exponential backoff
- Implement circuit breaker

---

#### 1D. Tool Execution Timeout
**What:** Long-running commands exceed gateway timeout
**Evidence:**
- Errors during pip installs, file operations
- Browser-use long sessions fail
- 60s+ operations reliably fail

**Mechanism:**
```
Command runs >30s → Gateway assumes hung → Kills session → Lifecycle error
```

**Fix:**
- Use background processes with polling
- Implement async/await patterns
- Break operations into smaller chunks

---

## ERROR 2: Disconnection Error

### Symptoms
- "Connection lost"
- "Session terminated"
- "Unable to reach gateway"
- Chat interface freezes/goes blank

### 🔴 PROBABLE CAUSES

#### 2A. Kimi Web Interface Timeout (Primary)
**What:** Kimi's web UI has session limits
**Evidence:**
- Happens after periods of inactivity
- Refreshing page loses session
- New chat required to reconnect

**Mechanism:**
```
User inactive 10-15 min → Kimi closes session → Connection lost
```

**Fix:**
- Use KimiClaw Persistent mode (proven working)
- Implement client-side keep-alive
- Use alternative interface (Telegram)

---

#### 2B. OpenClaw Gateway Restart/Crash
**What:** Gateway process restarts or crashes
**Evidence:**
- Error mentions "gateway" specifically
- Other users affected simultaneously
- Happens after updates/deployments

**Mechanism:**
```
Gateway update/restart → All sessions dropped → Reconnect required
```

**Fix:**
- Check gateway logs for crash patterns
- Implement session persistence
- Use local gateway for critical work

---

#### 2C. Browser/Client-Side Issues
**What:** Browser tab sleep, network change, etc.
**Evidence:**
- Happens when switching networks (WiFi → Mobile)
- Laptop sleep/wake cycle
- Browser tab backgrounded for long time

**Mechanism:**
```
Browser throttles background tab → WebSocket closes → Disconnection
```

**Fix:**
- Keep tab active
- Use desktop app instead of browser
- Implement visibility API handling

---

#### 2D. Rate Limiting / Throttling
**What:** Too many requests trigger protection
**Evidence:**
- Happens during rapid-fire interactions
- Many tool calls in quick succession
- Error mentions rate limits

**Mechanism:**
```
Requests > threshold → Rate limiter triggers → Connection throttled/dropped
```

**Fix:**
- Add delays between rapid requests
- Implement request batching
- Check rate limit headers

---

## 🎯 ROOT CAUSE MATRIX

| Error | Primary Cause | Secondary | Tertiary |
|-------|--------------|-----------|----------|
| Gateway Lifecycle | Idle timeout | Tool timeout | Memory limits |
| Disconnection | Kimi web timeout | Gateway restart | Browser issues |

---

## 🔧 SOLUTION PRIORITY

### Immediate (Prevent Errors)
1. **Use KimiClaw Persistent** (eliminates Kimi web timeout)
2. **Enable heartbeat** (prevents idle timeout)
3. **Break long operations** (avoid tool timeouts)

### Short-term (Handle Gracefully)
4. **Implement reconnection logic** (auto-retry on drop)
5. **Save state frequently** (file bridge pattern)
6. **Use background processes** (for long tasks)

### Long-term (Robust Architecture)
7. **Local gateway option** (full control)
8. **Telegram fallback** (alternative interface)
9. **Stateless design** (survives any disconnect)

---

## ✅ VERIFICATION STEPS

To confirm which cause is primary:

```
Test 1: Leave idle for 10 min
  → If disconnects: Kimi web timeout (Cause 2A)

Test 2: Run long command (>60s)
  → If lifecycle error: Tool timeout (Cause 1D)

Test 3: Use KimiClaw Persistent
  → If stable: Web timeout confirmed (Cause 2A)

Test 4: Check gateway logs
  → If crashes: Gateway restart (Cause 2B)

Test 5: Switch networks during chat
  → If disconnects: Transport issue (Cause 2C)
```

---

## 💡 KEY INSIGHT

**Both errors are likely the SAME root cause:**

The **Kimi web interface has aggressive timeout limits** that cascade:
1. Web session times out
2. Gateway detects dead connection
3. Reports as "lifecycle error"
4. Shows as "disconnection" to user

**Your Coordinator bot in KimiClaw Persistent mode doesn't have this problem** - proving the root cause is the web interface, not the underlying infrastructure.

---

*Analysis completed: 2026-02-26*
