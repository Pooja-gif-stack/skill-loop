def received_requests(request):
    receiver = UserProfile.objects.get(id=2)

    requests = SkillRequest.objects.filter(
        receiver=receiver
    ).order_by('-created_at')

    return render(
        request,
        'swap/received_requests.html',
        {'requests': requests}
    )