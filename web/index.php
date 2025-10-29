<?php
$apiBase = getenv('API_BASE') ?: 'http://185.245.61.161:8444/api/v1';
$healthUrl = rtrim($apiBase, '/') . '/instances';

$instances = [];
$error = null;

if (function_exists('curl_init')) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $healthUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Accept: application/json',
    ]);
    $response = curl_exec($ch);
    if ($response === false) {
        $error = curl_error($ch);
    } else {
        $decoded = json_decode($response, true);
        if (json_last_error() === JSON_ERROR_NONE) {
            $instances = $decoded;
        } else {
            $error = 'Invalid JSON response from API.';
        }
    }
    curl_close($ch);
} else {
    $error = 'cURL extension not available. Enable it to fetch API data.';
}
?>
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Minecraft Control Panel Übersicht</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</head>
<body class="bg-dark text-light">
<div class="container py-5">
    <h1 class="mb-4">Minecraft Control Panel Übersicht</h1>
    <?php if ($error): ?>
        <div class="alert alert-danger" role="alert">
            <?php echo htmlspecialchars($error, ENT_QUOTES, 'UTF-8'); ?>
        </div>
    <?php else: ?>
        <table class="table table-dark table-striped">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Typ</th>
                    <th>Software</th>
                    <th>Version</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
            <?php if (empty($instances)): ?>
                <tr>
                    <td colspan="5" class="text-center">Keine Instanzen gefunden.</td>
                </tr>
            <?php else: ?>
                <?php foreach ($instances as $instance): ?>
                    <tr>
                        <td><?php echo htmlspecialchars($instance['name'], ENT_QUOTES, 'UTF-8'); ?></td>
                        <td><?php echo htmlspecialchars($instance['instance_type'], ENT_QUOTES, 'UTF-8'); ?></td>
                        <td><?php echo htmlspecialchars($instance['software'], ENT_QUOTES, 'UTF-8'); ?></td>
                        <td><?php echo htmlspecialchars($instance['version'], ENT_QUOTES, 'UTF-8'); ?></td>
                        <td><?php echo htmlspecialchars($instance['status'], ENT_QUOTES, 'UTF-8'); ?></td>
                    </tr>
                <?php endforeach; ?>
            <?php endif; ?>
            </tbody>
        </table>
    <?php endif; ?>
</div>
</body>
</html>
