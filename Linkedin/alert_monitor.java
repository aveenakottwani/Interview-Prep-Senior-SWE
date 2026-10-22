public class AlertMonitor {

    private Queue<Integer>

    public enum SeverityLevel {
        LOW, MEDIUM, HIGH
    }

    public AlertMonitor() {
        // To Implement

    }

    /**
     * Record an alert with a timestamp and severity.
     *
     * @param currentTimestamp current time in seconds
     * @param severity         severity level of the alert
     */
    public void recordAlert(int currentTimestamp, SeverityLevel severity) {
        // To Implement
    }

    /**
     * Return the number of alerts received in the last 900 seconds (15 mins).
     *
     * @param currentTimestamp current time in seconds
     * @return int: The number of alerts in the last 15 minutes.
     */
    public int reportAlertsLast15Min(int currentTimestamp) {
        // To Implement
    }

    /**
     * Return the counts of 'low', 'medium', and 'high' severity alerts
     * within the current hour.
     * The "current hour" refers to the 60-minute (3600 seconds) block
     * containing the most recent timestamp.
     * For example, if most recent timestamp encountered is 3720, then this method
     * returns counts of all alerts that happened between 3600 and 7199 seconds.
     *
     * Example:
     *     // 0..3600 , 3601..7200, 7200..10240
     *     // 3200 (L:4, M:6, H:100)
     *
     * @param currentTimestamp current time in seconds
     * @return Map<SeverityLevel, Integer>: Counts by level
     */
    public Map<SeverityLevel, Integer> reportSeverityDistribution(int currentTimestamp) {
        // To Implement
    }

    /**
     * For each minute (in last 15 min data), return the index of the next minute
     * with greater alert volume to its right. If none exists, return -1 for that minute.
     * Note: each minute has at least one alert.
     *
     * Example:
     *     Minutes:      0, 1, 2, 3, 4, 5
     *     Counts:      [1, 2, 5, 2, 2, 1]
     *     Output:      [1, 2, -1, 4, -1, -1]
     *
     * @return List<Integer>: Indices of next minute spikes or -1
     */
    public List<Integer> detectAlertVolumeSpike() {
        // To Implement
    }
}


class Main{

    public static void main(String[] args){

    }
}