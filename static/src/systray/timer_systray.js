/** @odoo-module **/

import { Component, useState, onWillStart, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { user } from "@web/core/user";

// ── Quick-Start Dialog ────────────────────────────────────────────────────────

class TimerStartDialog extends Component {
    static template = "time_tracker.TimerStartDialog";
    static components = { Dialog };
    static props = {
        close: Function,
        onStarted: Function,
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.state = useState({
            projectId: false,
            taskId: false,
            description: "New Time Entry",
            projects: [],
            tasks: [],
            loading: false,
        });
        onWillStart(async () => {
            this.state.projects = await this.orm.searchRead(
                "project.project",
                [],
                ["id", "name"],
                { limit: 200, order: "name asc" }
            );
        });
    }

    async onProjectChange(ev) {
        const projectId = parseInt(ev.target.value) || false;
        this.state.projectId = projectId;
        this.state.taskId = false;
        this.state.tasks = [];
        if (projectId) {
            this.state.tasks = await this.orm.searchRead(
                "project.task",
                [["project_id", "=", projectId]],
                ["id", "name"],
                { limit: 200, order: "name asc" }
            );
        }
    }

    onTaskChange(ev) {
        this.state.taskId = parseInt(ev.target.value) || false;
    }

    onDescriptionChange(ev) {
        this.state.description = ev.target.value;
    }

    onCancel() {
        this.props.close();
    }

    async onStart() {
        if (this.state.loading) return;
        this.state.loading = true;
        try {
            const vals = { name: this.state.description || "New Time Entry" };
            if (this.state.projectId) vals.project_id = this.state.projectId;
            if (this.state.taskId) vals.task_id = this.state.taskId;
            const ids = await this.orm.create("time.entry", [vals]);
            const id = Array.isArray(ids) ? ids[0] : ids;
            await this.orm.call("time.entry", "action_start", [[id]]);
            this.props.onStarted();
            this.props.close();
        } finally {
            this.state.loading = false;
        }
    }
}

// ── Systray Component ─────────────────────────────────────────────────────────

class TimerSystray extends Component {
    static template = "time_tracker.TimerSystray";
    static props = {};

    setup() {
        this.orm = useService("orm");
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.state = useState({
            running: false,
            entryId: false,
            elapsed: "",
        });
        this._interval = null;

        onWillStart(() => this._fetchRunning());
        onWillUnmount(() => {
            if (this._interval) clearInterval(this._interval);
        });
    }

    async _fetchRunning() {
        const entries = await this.orm.searchRead(
            "time.entry",
            [["user_id", "=", user.userId], ["state", "=", "running"]],
            ["id", "start_datetime"],
            { limit: 1 }
        );
        if (entries.length) {
            const dtStr = entries[0].start_datetime.replace(" ", "T") + "Z";
            this._startInterval(entries[0].id, new Date(dtStr));
        } else {
            this._clearState();
        }
    }

    _startInterval(id, startTime) {
        this.state.running = true;
        this.state.entryId = id;
        this._tick(startTime);
        if (this._interval) clearInterval(this._interval);
        this._interval = setInterval(() => this._tick(startTime), 1000);
    }

    _tick(startTime) {
        const total = Math.max(0, Math.floor((Date.now() - startTime) / 1000));
        const h = Math.floor(total / 3600);
        const m = Math.floor((total % 3600) / 60);
        const s = total % 60;
        this.state.elapsed = `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
    }

    _clearState() {
        this.state.running = false;
        this.state.entryId = false;
        this.state.elapsed = "";
        if (this._interval) {
            clearInterval(this._interval);
            this._interval = null;
        }
    }

    onClick() {
        if (this.state.running) {
            this._stop();
        } else {
            this.dialog.add(TimerStartDialog, {
                onStarted: () => this._fetchRunning(),
            });
        }
    }

    async _stop() {
        await this.orm.call("time.entry", "action_stop", [[this.state.entryId]]);
        this._clearState();
        this.notification.add("Timer gestoppt.", { type: "success" });
    }
}

registry.category("systray").add("time_tracker.timer_systray", {
    Component: TimerSystray,
}, { sequence: 1 });
