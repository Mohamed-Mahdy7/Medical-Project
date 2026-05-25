from django.utils.timezone import now

from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser
)

from rest_framework.decorators import action

from rest_framework.response import Response

from rest_framework import status

from .models import (
    Specialty,
    DoctorProfile
)

from appointments.models import (
    Appointment
)

from .serializers import (
    SpecialtySerializer,
    DoctorListSerializer,
    DoctorDetailSerializer,
    DoctorUpdateSerializer,
    DoctorAppointmentSerializer
)

from .permissions import (
    IsDoctorOwnerOrAdmin
)


class SpecialtyViewSet(
    ReadOnlyModelViewSet
):

    queryset = Specialty.objects.all()

    serializer_class = SpecialtySerializer

    permission_classes = [AllowAny]


class DoctorViewSet(ModelViewSet):

    queryset = DoctorProfile.objects.select_related(
        'user',
        'specialty'
    )

    permission_classes = [
        IsDoctorOwnerOrAdmin
    ]


    
    def get_serializer_class(self):

         
        if self.action == 'list':

            return DoctorListSerializer
 
        elif self.action in [
            'retrieve',
            'me'
        ]:

            return DoctorDetailSerializer
 
        elif self.action == 'appointments':

            return DoctorAppointmentSerializer

         
        return DoctorUpdateSerializer


     
    def get_permissions(self):

       
        if self.action in [
            'list',
            'retrieve'
        ]:

            return [AllowAny()]

        
        elif self.action in [
            'destroy',
            'approve',
            'block'
        ]:

            return [IsAdminUser()]

         
        return [IsAuthenticated()]


     
    def get_queryset(self):

        queryset = super().get_queryset()
 
        if not self.request.user.is_staff:

            queryset = queryset.filter(
                is_approved=True,
                is_blocked=False
            )

        
        specialty = self.request.query_params.get(
            'specialty'
        )

        if specialty:

            queryset = queryset.filter(
                specialty__id=specialty
            )
 
        name = self.request.query_params.get(
            'name'
        )

        if name:

            queryset = queryset.filter(
                user__first_name__icontains=name
            )

        return queryset


     
    def update(
        self,
        request,
        *args,
        **kwargs
    ):

        doctor = self.get_object()
 
        if not request.user.is_staff:

            if doctor.user != request.user:

                return Response(

                    {
                        'error': 'Not allowed'
                    },

                    status=status.HTTP_403_FORBIDDEN
                )

        return super().update(
            request,
            *args,
            **kwargs
        )


 
    def partial_update(
        self,
        request,
        *args,
        **kwargs
    ):

        doctor = self.get_object()

        if not request.user.is_staff:

            if doctor.user != request.user:

                return Response(

                    {
                        'error': 'Not allowed'
                    },

                    status=status.HTTP_403_FORBIDDEN
                )

        return super().partial_update(
            request,
            *args,
            **kwargs
        )


    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(
        self,
        request
    ):

        serializer = self.get_serializer(
            request.user.doctor_profile
        )

        return Response(serializer.data)


    
    @action(
        detail=True,
        methods=['patch'],
        permission_classes=[IsAdminUser]
    )
    def approve(
        self,
        request,
        pk=None
    ):

        doctor = self.get_object()

        doctor.is_approved = True

        doctor.save()

        return Response(
            {
                'message': 'Doctor approved'
            }
        )


 
    @action(
        detail=True,
        methods=['patch'],
        permission_classes=[IsAdminUser]
    )
    def block(
        self,
        request,
        pk=None
    ):

        doctor = self.get_object()

        doctor.is_blocked = True

        doctor.save()

        return Response(
            {
                'message': 'Doctor blocked'
            }
        )


    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def appointments(
        self,
        request
    ):

        queryset = Appointment.objects.filter(
            doctor__user=request.user
        )

       
        appointment_status = request.query_params.get(
            'status'
        )

        if appointment_status:

            queryset = queryset.filter(
                status=appointment_status
            )
 
        appointment_type = request.query_params.get(
            'type'
        )

        if appointment_type == 'upcoming':

            queryset = queryset.filter(
                date__gte=now().date()
            )

        elif appointment_type == 'past':

            queryset = queryset.filter(
                date__lt=now().date()
            )

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(serializer.data)


    
    @action(
        detail=True,
        methods=['patch'],
        permission_classes=[IsAuthenticated]
    )
    def appointment_status(
        self,
        request,
        pk=None
    ):

        appointment = Appointment.objects.get(
            id=pk
        )
 
        if appointment.doctor.user != request.user:

            return Response(

                {
                    'error': 'Not allowed'
                },

                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get(
            'status'
        )

        
        if new_status not in [
            'confirmed',
            'rejected',
            'completed'
        ]:

            return Response(

                {
                    'error': 'Invalid status'
                },

                status=status.HTTP_400_BAD_REQUEST
            )

        appointment.status = new_status

        appointment.save()

        return Response(
            {
                'message': f'Appointment {new_status}'
            }
        )

 
    @action(
        detail=True,
        methods=['patch'],
        permission_classes=[IsAuthenticated]
    )
    def add_note(
        self,
        request,
        pk=None
    ):

        appointment = Appointment.objects.get(
            id=pk
        )

        if appointment.doctor.user != request.user:

            return Response(

                {
                    'error': 'Not allowed'
                },

                status=status.HTTP_403_FORBIDDEN
            )

        appointment.note = request.data.get(
            'note'
        )

        appointment.save()

        return Response(
            {
                'message': 'Note added'
            }
        )